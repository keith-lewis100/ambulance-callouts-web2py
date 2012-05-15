@auth.requires_login()
def index():
    form = SQLFORM.factory(
        Field('date', 'date'),
        Field('ambulance', default=session.ambulance,
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'ambulance.id',
                                            db.ambulance._format))))
    if form.process().accepted:
        response.flash = 'form accepted'
        session.date = form.vars.date
        session.ambulance = form.vars.ambulance
        redirect(URL('shift.html'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def shift():
    """
return the shift table or edit/create form
    """
    query = db.shift.id > 0
    if session.date:
        query = query & (db.shift.call_date == session.date)
        db.shift.call_date.default = session.date
    if session.ambulance:
        query = query & (db.shift.ambulance == session.ambulance)
        db.shift.ambulance.default = session.ambulance

    grid = SQLFORM.grid(query, fields=[db.shift.id, db.shift.date, db.shift.start_time, 
                 db.shift.ambulance, db.shift.driver], csv=False, 
                 searchable=False, ui='jquery-ui')
    return dict(grid=grid)
