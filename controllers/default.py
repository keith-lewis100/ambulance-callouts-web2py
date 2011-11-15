# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    form = SQLFORM.factory(
        Field('date', 'date'),
        Field('facility', requires=IS_EMPTY_OR(IS_IN_DB(db, 'facility.id',
                                                        db.facility._format))),
        Field('ambulance', requires=IS_EMPTY_OR(IS_IN_DB(db, 'ambulance.id',
                                                         db.ambulance._format))))
    if form.process().accepted:
        response.flash = 'form accepted'
        session.date = form.vars.date
        session.facility = form.vars.facility
        session.ambulance = form.vars.ambulance
        redirect(URL('journey.html'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def journey():
    """
return the journey table or edit/create form
    """
    can_modify = auth.has_membership(role='journey_editor')
    query = db.journey.id > 0
    if session.date:
        query = query & (db.journey.call_date == session.date)
    if session.facility:
        query = query & (db.journey.facility == session.facility)
    if session.ambulance:
        query = query & (db.journey.ambulance == session.ambulance)
    journeys = SQLFORM.grid(query, fields=[db.journey.id, db.journey.call_date, db.journey.hc_time, db.journey.family_name,
                                           db.journey.ambulance, db.journey.condition], create=can_modify, editable=can_modify,
                            deletable=can_modify, csv=False, searchable=False, ui='jquery-ui')
    return dict(journeys=journeys)

def clinician():
    clinicians = SQLFORM.grid(db.clinician.id > 0, csv=False, searchable=False, ui='jquery-ui')
    return dict(table=clinicians)

def user(): return dict(form=auth())
