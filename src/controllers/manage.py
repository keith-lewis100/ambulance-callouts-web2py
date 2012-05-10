# -*- coding: utf-8 -*-

def ambulance():
    return name_grid(db.ambulance)

def action():
    return name_grid(db.action)

def condition():
    table = db.condition
    grid = SQLFORM.grid(table.id > 0, 
                              fields=[table.id, table.title], 
                              csv=False, searchable=False, ui='jquery-ui')
    return dict(grid=grid)

def facility():
    return name_grid(db.facility)

def name_grid(table):
    """
return the ambulance table or edit/create form
    """
    grid = SQLFORM.grid(table.id > 0, 
                              fields=[table.id, table.name], 
                              csv=False, searchable=False, ui='jquery-ui')
    return dict(grid=grid)
