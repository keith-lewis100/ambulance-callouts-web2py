# -*- coding: utf-8 -*-

#import widgets

# fields listed child first
def buildSelect(value, depth, typeField, wrapper):
    if depth==0: return
    parentValue = None
    options = [OPTION('', _value=0, _class='static')]
    rows = db(typeField == depth).select()
    for row in rows:
        k = row.id
        optClass = 'sub_' + str(row.parent)
        options.append(OPTION(row.name, _value=k, _class=optClass))
        if k == value:
            parentValue = row.parent
    buildSelect(parentValue, depth-1, typeField, wrapper)
    wrapper.append(SELECT(*options))
    return 

class CascadingSelect(FormWidget):
    def __init__(self, depth, typeField):
        self.depth = depth
        self.typeField = typeField
        
    def widget(self, field, value, **attributes):
        tableId = '%s_%s_cascade' % (field._tablename, field.name)
        wrapper = TABLE(_id = tableId)
        buildSelect(value, self.depth, self.typeField, wrapper)
        return wrapper
      
def index():
    cascadeWidget=CascadingSelect(4, db.location.type)
    form = SQLFORM.factory(
        Field('village',
              requires=IS_IN_DB(db, 'location.id', db.location._format),
#              widget=cascadeWidget.widget,
              default=3))
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    response.files.append(URL('static', 'js/cascade.js'))
    return dict(form=form)

def add():
   form = SQLFORM(db.location)
   if form.accepts(request):
      response.flash = 'Added'
   elif form.errors:
      response.flash = 'form has errors'
   return dict(form=form)
