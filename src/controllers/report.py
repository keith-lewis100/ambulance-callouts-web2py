def index():
    form = SQLFORM.factory(
        Field('start_date', 'date', requires=IS_DATE()),
        Field('end_date', 'date', requires=IS_DATE()),
        Field('station',
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'facility.id',
                                            db.facility._format))),
        Field('format', default='html', requires=IS_IN_SET(['html', 'csv', 'ods'])))

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

def journeys_by_condition(query):
    count = db.journey.id.count()
    rows = db(query).select(db.shift.date, db.journey.condition, count,
                            groupby=db.shift.date|db.journey.condition)
    return rows.as_list()

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
    table=journeys_raw(query)
    return dict(table=table)
