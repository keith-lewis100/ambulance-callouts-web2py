from datetime import timedelta

@auth.requires_login()
def index():
    form = SQLFORM.factory(
        Field('date', 'date', requires=IS_DATE(), comment='date in week'),
        Field('station', default=session.station, comment='leave blank unless only interested in one station',
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'facility.id',
                                            db.facility._format))))

    if form.process().accepted:
        response.flash = 'search started'
        weekday = timedelta(form.vars.date.weekday())
        session.date = form.vars.date - weekday # find start of week
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
        del request.vars.daydelta
    # find all shifts for the specified week
    nextweek = session.date + timedelta(7)
    query = (db.shift.date >= session.date) & (db.shift.date < nextweek)
    db.shift.date.default = session.date # default to mondays date

    session.shift = None # reset here - the user will then set it by selecting a shift
    stationname = T('Any')

    if session.station:
        query = query & (db.shift.station == session.station)
        db.shift.station.default = session.station
        stationname = db.facility[session.station].name
        
    # dont ask user to enter ambulance instead take it from the station
    db.shift.ambulance.default = db(db.ambulance.id > 0).select().first().id
    if len(request.args)>1 and request.args[-2]=='new' and request.vars.station:
        request.vars.ambulance = db.facility[int(request.vars.station)].stationed_ambulance

    grid = SQLFORM.grid(query, fields=[db.shift.id, db.shift.date, db.shift.start_time, 
                 db.shift.station, db.shift.driver], csv=False,
                 searchable=False, ui='jquery-ui', links=[link_journeys],
                 sortable=True)
    return dict(station=stationname,date=session.date,grid=grid)
