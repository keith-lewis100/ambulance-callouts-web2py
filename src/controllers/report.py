import datetime

def index():
    form = SQLFORM.factory(
        Field('start_date', 'date', requires=IS_DATE()),
        Field('end_date', 'date', requires=IS_DATE()),
        Field('station',
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'facility.id',
                                            db.facility._format))),
        Field('format', default='csv',
              requires=IS_IN_SET(['html', 'csv', 'ods'])))

    if form.process().accepted:
        response.flash = 'report launched'
        parms = { 'start_date': form.vars.start_date,
                  'end_date': form.vars.end_date }
        if form.vars.station:
            parms['station'] = str(form.vars.station)
        redirect(URL('report.%s' % form.vars.format, vars=parms))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)    

def month_of_date(date):
    return date.year * 12 + date.month

def journeys_by_condition(query, start_month, end_month):
    count = db.journey.id.count()
    records = db(query).select(db.shift.date, db.journey.condition, count,
                            groupby=db.shift.date|db.journey.condition)
    count_map = {}
    for record in records:
        key = (month_of_date(record.shift.date), record.journey.condition)
        if not count_map.has_key(key):
            count_map[key] = 0
        count_map[key] += record[count]
    headers = ['Condition']
    for month in range(start_month, end_month + 1):
        date = datetime.date(month/12, month % 12, 1)
        headers.append(date.strftime("%B %y"))
    table = [headers]
    for cond in db(db.condition.id > 0).select():
        row = [cond.title]
        for month in range(start_month, end_month + 1):
            val = 0
            if count_map.has_key((month, cond.id)):
                val = count_map[(month, cond.id)]
            row.append(val)
        table.append(row)
    return table

def journeys_raw(query):
    rows = db(query).select(db.shift.date,
                         db.shift.station,
                         db.journey.age,
                         db.journey.sex,
                         db.journey.used_stretcher,
                         db.journey.used_cycle,
                         db.journey.maternity,
                         db.journey.condition,
                         db.journey.amb_action,
                         db.journey.facility, orderby=db.shift.date)
    return rows

def report():
    query = (db.journey.shift == db.shift.id) & \
            (db.shift.date >= request.vars.start_date) & \
            (db.shift.date <= request.vars.end_date)
    if request.vars.station:
        query &= db.shift.station == int(request.vars.station)
    start_month = month_of_date(datetime.datetime.strptime(request.vars.start_date,
                                                       "%Y-%m-%d"))
    end_month = month_of_date(datetime.datetime.strptime(request.vars.end_date,
                                                     "%Y-%m-%d"))
    table=journeys_by_condition(query, start_month, end_month)
    return dict(table=table, filename='report')
