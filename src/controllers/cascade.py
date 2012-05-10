# -*- coding: utf-8 -*-

#import widgets

# fields listed child first
def buildSelect(fields, value, wrapper):
    if len(fields) == 0: return str(value)
    field = fields[0]
    parentValue = ''
    requires = field.requires
    options = []
    for (k, v) in requires.options(True):
        optClass = 'static'
        if isinstance(v, tuple):
            optClass = 'sub_' + str(v[0])
            if k == str(value):
                parentValue = v[0]
            v = v[1]
        options.append(OPTION(v, _value=k, _class=optClass))

    r = buildSelect(fields[1:], parentValue, wrapper)
    r = r + "/" + str(value)
    
    attr = FormWidget._attributes(field, {'value': value})
    wrapper.append(SELECT(*options, **attr))
    return r

class CascadingSelect(FormWidget):
    def __init__(self, parents):
        self.parents = parents
        
    def widget(self, field, value, **attributes):
        tableId = '%s_%s_cascade' % (field._tablename, field.name)
        wrapper = TABLE(_id = tableId)
        fields = [ field ] + self.parents
        r = buildSelect(fields, value, wrapper)
        wrapper.append(XML("r = " + r))
        return wrapper

def index():
    cascadeWidget=CascadingSelect([db.village.parish,
                        db.parish.subCounty, db.subCounty.district])
    form = SQLFORM.factory(
        Field('village',
              requires=IS_IN_DB(db, 'village.id', db.village._format),
              widget=cascadeWidget.widget,
              default=3))
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    response.files.append(URL('static', 'js/cascade.js'))
    return dict(form=form)
