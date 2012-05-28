# -*- coding: utf-8 -*-

def journey():
    """
return the journey table or edit/create form
    """
    can_modify = auth.has_membership(role='journey_editor')
    shift = request.vars.shift
    query = db.journey.shift == shift
    db.journey.shift.default = shift

    grid = SQLFORM.grid(query, 
                            fields=[db.journey.id, db.journey.dispatch_time,
                                    db.journey.family_name, db.journey.age,
                                    db.journey.condition, db.journey.facility], 
                            create=can_modify, editable=can_modify, deletable=can_modify, 
                            csv=False, searchable=False, ui='jquery-ui')
    return dict(journeys=grid)
