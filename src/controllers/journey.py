# -*- coding: utf-8 -*-

#from widgets import CascadingSelect

class CascadingSelect(FormWidget):
    def __init__(self, typeField, labels):
        self.labels = labels
        self.typeField = typeField

    def buildSelect(self, loctype, value, baseid):
        dbconn = self.typeField._table._db
        null_option = "Select " + self.labels[loctype-1]
        options = [OPTION(null_option, _value='', _class='static')]
        rows = dbconn(self.typeField == loctype).select()
        for row in rows:
            k = row.id
            optClass = 'sub_' + str(row.parent)
            options.append(OPTION(row.name, _value=k, _class=optClass))
        return SELECT(*options,
                      value=value,
                      _class='reference',
                      _id = baseid + str(loctype))

    def createScript(self, baseid):
        js = "$(function(){"
        js += "cascadeTable = $('#%stable');" % baseid
        js += "createCascade(cascadeTable, %s, '%s');" % (len(self.labels), baseid)
        js += "});"
        return SCRIPT(js, _type="text/javascript")
        
    def buildValueList(self, table, value):
        depth = len(self.labels)
        values = [None] * depth
        v = value
        for loctype in range(depth-1, -1, -1):
            values[loctype] = v
            row = table(v)
            if row == None: break
            v = row.parent
        return values
    
    def widget(self, field, value, **attributes):
        baseid = '%s_%s_' % (field._tablename, field.name)
        table = TABLE(_id = baseid + 'table')
        values = self.buildValueList(self.typeField._table, value)
        for loctype in range(1, len(values)+1):
            select = self.buildSelect(loctype, values[loctype-1], baseid)
            table.append(select)
        select.update(_name=field.name) # ensure last select uses field name
        js = self.createScript(baseid)
        wrapper = DIV([table, js])
        return wrapper

@auth.requires_membership('journey_editor')
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
    db.journey.facility.default = r.station
    cascadeWidget = CascadingSelect(db.location.type,
            ['district', 'sub-county', 'parish', 'village'])
    db.journey.patient_location.widget = cascadeWidget.widget
    grid = SQLFORM.grid(query, 
                            fields=[db.journey.id, db.journey.dispatch_time,
                                    db.journey.family_name, db.journey.age,
                                    db.journey.condition, db.journey.facility], 
                             csv=False, searchable=False, ui='jquery-ui')
    response.files.append(URL('static', 'js/cascade.js'))
    # return values to render in the view
    return dict(back=shiftlink, shift=shiftname, grid=grid)
