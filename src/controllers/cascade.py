# -*- coding: utf-8 -*-

#import widgets

def buildSelect(field, value, wrapper):
    requires = field.requires
    options = []
    for (k, v) in requires.options(True):
        optClass = 'static'
        if isinstance(v, tuple):
            optClass = 'sub_' + str(v[0])
            v = v[1]
        options.append(OPTION(v, _value=k, _class=optClass))

    attr = FormWidget._attributes(field, {'value': value})
    wrapper.append(SELECT(*options, **attr))

class CascadingSelect(FormWidget):
    def __init__(self, *parents):
        self.parents = parents
        
    def widget(self, field, value, **attributes):
        tableId = '%s_%s_cascade' % (field._tablename, field.name)
        wrapper = TABLE(_id = tableId)
        for parent in self.parents:
            buildSelect(parent, '', wrapper)
        buildSelect(field, value, wrapper)
        return wrapper

def index():
    cascadeWidget=CascadingSelect(db.subCounty.district, db.parish.subCounty,
                                  db.village.parish)
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
