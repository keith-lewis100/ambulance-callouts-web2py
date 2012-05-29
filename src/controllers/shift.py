from datetime import timedelta

@auth.requires_login()
def index():
    form = SQLFORM.factory(
        Field('date', 'date', requires=IS_DATE()),
        Field('station', default=session.station),
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'facility.id',
                                            db.facility._format)))

    if form.process().accepted:
        response.flash = 'form accepted'
        session.date = form.vars.date
        session.station = form.vars.station
        redirect(URL('shifts'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def link_journeys(r):
    return A('goto journeys', _href=URL('journey', 'journey', vars=dict(shift=r.id)))

def shifts():
    """
return the shift table or edit/create form
    """
    if request.vars.daydelta:
        delta = timedelta(int(request.vars.daydelta))
        session.date = session.date + delta
    query = (db.shift.date == session.date)

    db.shift.date.default = session.date
    if session.station:
        query = query & (db.shift.station == session.station)
        db.shift.station.default = session.station
        db.shift.ambulance.default = db.facility[session.station].stationed_ambulance        
    stationname = T('Any')
    if session.station:
        stationname = db.facility[session.station].name
    grid = SQLFORM.grid(query, fields=[db.shift.id, db.shift.date, db.shift.start_time, 
                 db.shift.station, db.shift.driver], csv=False, 
                 searchable=False, ui='jquery-ui', links=[link_journeys])
    return dict(ambulance=stationname,date=session.date,grid=grid)
