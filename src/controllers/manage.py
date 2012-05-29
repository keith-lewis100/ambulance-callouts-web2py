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
    grid = SQLFORM.grid(table.id > 0, 
                              csv=False, searchable=False, ui='jquery-ui')
    return dict(grid=grid)
