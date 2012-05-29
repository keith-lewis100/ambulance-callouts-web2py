# -*- coding: utf-8 -*-

def journey():
    """
return the journey table or edit/create form
    """
    # on first entry we should have the shift var
    if request.vars.shift:
        session.shift = request.vars.shift

    # add a link back to the shift search results
    shiftlink = A('return to shift list', _href=URL('shift', 'shifts'))

    # now find the shift name
    r = db.shift[session.shift]
    shiftname = '%s on %s at %s' % (r.station.name, r.date, r.start_time)

    # create the grid
    query = (db.journey.shift == session.shift)
    db.journey.shift.default = session.shift
    can_modify = auth.has_membership(role='journey_editor')
    grid = SQLFORM.grid(query, 
                            fields=[db.journey.id, db.journey.dispatch_time,
                                    db.journey.family_name, db.journey.age,
                                    db.journey.condition, db.journey.facility], 
                            create=can_modify, editable=can_modify, deletable=can_modify, 
                            csv=False, searchable=False, ui='jquery-ui')
    # return values to render in the view
    return dict(back=shiftlink, shift=shiftname,grid=grid)
