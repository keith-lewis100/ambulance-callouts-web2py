def index():
    form = SQLFORM.factory(
        Field('start_date', 'date', requires=IS_DATE()),
        Field('end_date', 'date', requires=IS_DATE()),
        Field('station',
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'facility.id',
                                            db.facility._format))))

    if form.process().accepted:
        response.flash = 'report launched'
        redirect(URL('journeys_by_condition.html', vars=form.vars))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)    

def journeys_by_condition():
    query = (db.journey.shift == db.shift.id) & \
            (db.shift.date >= request.vars.start_date) & \
            (db.shift.date <= request.vars.end_date)
#    if request.vars.station:
#        query &= db.shift.station == request.vars.station
    count = db.journey.id.count()
    rows = db(query).select(db.shift.date, db.journey.condition, count,
                            groupby=db.shift.date|db.journey.condition)
    return dict(table=rows)
