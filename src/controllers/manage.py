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
