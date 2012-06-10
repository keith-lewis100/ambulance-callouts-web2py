# -*- coding: utf-8 -*-

from sqlhtml import FormWidget

from html import TABLE, OPTION, SELECT

class CascadingSelect(FormWidget):
    def __init__(self, depth, typeField):
        self.depth = depth
        self.typeField = typeField

    def buildSelect(self, loctype, value, baseid):
        dbconn = self.typeField._table._db
        options = [OPTION('', _value='', _class='static')]
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
        js += "createCascade(cascadeTable, %s, '%s');" % (self.depth, baseid)
        js += "});"
        return SCRIPT(js, _type="text/javascript")
        
    def buildValueList(self, table, value):
        values = [None] * self.depth
        v = value
        for loctype in range(self.depth-1, -1, -1):
            values[loctype] = v
            row = table(v)
            if row == None: break
            v = row.parent
        return values
    
    def widget(self, field, value, **attributes):
        baseid = '%s_%s_' % (field._tablename, field.name)
        table = TABLE(_id = baseid + 'table')
        values = self.buildValueList(self.typeField._table, value)
        for loctype in range(1, self.depth+1):
            select = self.buildSelect(loctype, values[loctype-1], baseid)
            table.append(select)
        select.update(_name=field.name) # ensure last select uses field name
        js = self.createScript(baseid)
        wrapper = DIV([table, js])
        return wrapper
