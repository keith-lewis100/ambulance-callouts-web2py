# -*- coding: utf-8 -*-

@auth.requires_login()
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
    return {'grid' : grid }

locplurals = ['districts', 'sub-counties', 'parishes', 'villages']
locnames = ['district', 'sub-county', 'parish', 'village']
            
def location():
    """
return the grid for the specified table
    """
    nargs = 0
    parentid = None
    breadcrumbs = [A('All Districts', _href=URL('location')), ' > ']
    # find last id in args - they start with underscore
    # build breadcrumbs list as we go
    while len(request.args)>nargs:
        key = request.args(nargs)
        if not key.startswith('_'):
            break
        parentid = key[1:]
        name = db.location(parentid).name
        nargs += 1
        breadcrumbs += [A(name, _href=URL(args=request.args[:nargs])), ' > ']

    # ensure new locations have the correct parent and type
    db.location.parent.default = parentid
    db.location.type.default = nargs + 1
    
    # now define the header
    loctype = locplurals[nargs]

    links = []
    if nargs<3:
        links.append(lambda row : A(locplurals[nargs+1],
                _href=URL(args=request.args[:nargs] + ['_' + str(row.id)])))
    query = (db.location.parent == parentid)
    db.location.id.readable = False # supress display of id column
    db.location.parent.readable = False # supress display of parent
    db.location.parent.writable = False
    db.location.type.readable = False # supress display of type
    db.location.type.writable = False
    grid = SQLFORM.grid(query, args=request.args[:nargs],
                        fields=[db.location.id, db.location.name],
                        details=False, searchable=False,
                        ui='jquery-ui', links=links)
    return { 'breadcrumbs': DIV(*breadcrumbs), 'heading': loctype,
             'content': grid}
