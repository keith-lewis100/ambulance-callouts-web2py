import datetime

class Month:
    def __init__(self, date):
        self.index = 12*date.year + date.month

    def __add__(self, offset):
        m = self.index + offset
        date = datetime.date(m / 12, m % 12, 1)
        return Month(date)

    def __cmp__(self, other):
        return self.index - other.index

    def __hash__(self):
        return self.index

    def strf(self, format):
        date = datetime.date(self.index/12, self.index % 12, 1)
        return date.strftime(format)
    
class MonthRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __getitem__(self, index):
        m = self.start + index
        if m >= self.end:
            raise IndexError()
        return m
    
@auth.requires_login()
def index():
    form = SQLFORM.factory(
        Field('start_date', 'date', requires=IS_DATE()),
        Field('end_date', 'date', requires=IS_DATE()),
        Field('station',
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'facility.id',
                                            db.facility._format))),
        Field('format', default='csv',
              requires=IS_IN_SET(['html', 'csv'])))

    if form.process().accepted:
        response.flash = 'report launched'
        parms = { 'start_date': form.vars.start_date,
                  'end_date': form.vars.end_date }
        if form.vars.station:
            parms['station'] = str(form.vars.station)
        redirect(URL('report', extension=form.vars.format,
                     args=request.args,
                     vars=parms))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)    

def journeys_by_condition(query, start_month, end_month):
    count = db.journey.id.count()
    records = db(query).select(db.shift.date, db.journey.condition, count,
                            groupby=db.shift.date|db.journey.condition)
    count_map = {}
    for record in records:
        key = (Month(record.shift.date), record.journey.condition)
        if not count_map.has_key(key):
            count_map[key] = 0
        count_map[key] += record[count]
    headers = ['Condition']
    for month in MonthRange(start_month, end_month + 1):
        headers.append(month.strf("%B %y"))
    table = [headers]
    for cond in db(db.condition.id > 0).select():
        row = [cond.title]
        for month in MonthRange(start_month, end_month + 1):
            val = 0
            if count_map.has_key((month, cond.id)):
                val = count_map[(month, cond.id)]
            row.append(val)
        table.append(row)
    return table

def journeys_raw(query):
    records = db(query).select(db.shift.date,
                         db.shift.station,
                         db.journey.age,
                         db.journey.sex,
                         db.journey.used_stretcher,
                         db.journey.used_cycle,
                         db.journey.pregnant,
                         db.journey.condition,
                         db.journey.amb_action,
                         db.journey.facility, orderby=db.shift.date)
    table = [ records.colnames ]
    for record in records:
        row = []
        for col in records.colnames:
            v = record[col]
            (t, f) = col.split('.')
            field = db[t][f]
            if field.type.startswith('reference'):
                v = represent(field, v, record)
            row.append(v)
        table.append(row)
    return table

@auth.requires_login()
def report():
    report = request.args[0]
    start_date = datetime.datetime.strptime(request.vars.start_date,
                                                       "%Y-%m-%d")
    end_date = datetime.datetime.strptime(request.vars.end_date,
                                                     "%Y-%m-%d")
    query = (db.journey.shift == db.shift.id) & \
            (db.shift.date >= start_date) & \
            (db.shift.date <= end_date)
    if request.vars.station:
        query &= db.shift.station == int(request.vars.station)
    if report == 'journey_records':
        table = journeys_raw(query)
    else:
        table = journeys_by_condition(query, Month(start_date), Month(end_date))
    return dict(table=table, report=report)
