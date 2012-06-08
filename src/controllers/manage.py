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
    return {'grid' : grid }

locplurals = ['districts', 'sub-counties', 'parishes', 'villages']
locnames = ['district', 'sub-county', 'parish', 'village']
            
def location():
    """
return the grid for the specified table
    """
    # add a link back to the previous level results
    backlink = ''
#        backlink = A('return to previous list', _href=URL('location',
#                            vars=dict(back = 'y')))
    nargs = 0
    parentid = None
    while len(request.args)>nargs:
        key = request.args(nargs)
        if not key.startswith('_'):
            break
        parentid = key[1:]
        nargs += 1
        
    # now find the parent name
    parentname = ''
#        parentname = db.location[parentid]._format()
    links = []
    if nargs<3:
        links.append(lambda row : A(locplurals[nargs+1],
                _href=URL(args=request.args[:nargs] + ['_' + str(row.id)])))
    query = (db.location.parent == parentid)
    db.location.id.readable = False # supress display of id column
    grid = SQLFORM.grid(query, args=request.args[:nargs],
                        fields=[db.location.id, db.location.name],
                        details=False, searchable=False,
                        ui='jquery-ui', links=links)
    return { 'back': backlink, 'parentname': parentname, 'grid': grid}
