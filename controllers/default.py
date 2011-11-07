# -*- coding: utf-8 -*-

def index():
    form = SQLFORM.factory(
        Field('date', 'datetime'),
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

@auth.requires_login()
def journey():
    """
return the journey table or edit/create form
    """
    can_modify = auth.has_membership(role='journey_editor')
    journeys = SQLFORM.grid(db.journey.id > 0, fields=[db.journey.id, db.journey.call_time, db.journey.ambulance, 
                            db.journey.family_name, db.journey.condition], create=can_modify, editable=can_modify, deletable=can_modify,
                            csv=False, searchable=False, ui='jquery-ui')
    return dict(journeys=journeys)
    
def user(): return dict(form=auth())

