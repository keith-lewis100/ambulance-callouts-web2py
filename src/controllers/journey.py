# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    form = SQLFORM.factory(
        Field('facility', default=session.facility,
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'facility.id',
                                                        db.facility._format))),
        Field('shift', default=session.shift,
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'shift.id',
                                                         db.shift._format))))
    if form.process().accepted:
        response.flash = 'form accepted'
        session.facility = form.vars.facility
        session.shift = form.vars.shift
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
    if session.facility:
        query = query & (db.journey.facility == session.facility)
        db.journey.facility.default = session.facility 
    if session.shift:
        query = query & (db.journey.shift == session.shift)
        db.journey.shift.default = session.shift

    journeys = SQLFORM.grid(query, 
                            fields=[db.journey.id, db.journey.hc_time,
                                    db.journey.family_name, db.journey.shift, db.journey.condition],
                            create=can_modify, editable=can_modify, deletable=can_modify, 
                            csv=False, searchable=False, ui='jquery-ui')
    return dict(journeys=journeys)
