# -*- coding: utf-8 -*-

def table():
    """
return the grid for the specified table
    """
    table_name = request.args[0]
    if not table_name in ['condition', 'action', 'ambulance', 'driver',
                       'facility']:
       return "invalid table"
    table = db[table_name]
    grid = SQLFORM.grid(table.id > 0, args=request.args[:1],
                        details=False, searchable=False, ui='jquery-ui',
                        maxtextlength=30, maxtextlengths={'condition.title': 80,
                                                          'action.name' : 80})
    return dict(grid=grid)

def link_locations(r):
    return A('show next level', _href=URL('location',
                                          vars=dict(parentid = r.id)))

def location():
    """
return the grid for the specified table
    """
    if not session.location_ids:
        session.location_ids = [None]
        session.loctype = 0
    if request.vars.back:
        session.loctype = session.loctype - 1
    if request.vars.parentid:
        session.location_ids[session.loctype] = request.vars.parentid
        session.loctype = session.loctype + 1
    loctype = session.loctype
    parentid = session.location_ids[loctype]
    # add a link back to the previous level results
    backlink = ''
    if loctype > 0:
        backlink = A('return to previous list', _href=URL('location',
                            vars=dict(back = 'y')))

    # now find the parent name
    parentname = ''
    if parentid:
        parentname = db.location[parentid]._format()
    
    query = (db.location.parent == parentid)
    db.location.id.readable = False # supress display of id column
    grid = SQLFORM.grid(query, fields=[db.location.id, db.location.name], details=False, searchable=False,
                        ui='jquery-ui', links=[link_locations])
    return { 'back': backlink, 'parentname': parentname, 'grid': grid}
