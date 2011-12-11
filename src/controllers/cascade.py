# -*- coding: utf-8 -*-

#import widgets

def buildSelect(field, value, wrapper):
        default = dict(value=value)
        attr = FormWidget._attributes(field, default)
        requires = field.requires
        options = []
        for (k, v) in requires.options(True):
            optClass = 'static'
            if isinstance(v, tuple):
                optClass = 'sub_' + str(v[0])
                v = v[1]
            options.append(OPTION(v, _value=k, _class=optClass))

        wrapper.append(SELECT(*options, **attr))

class CascadingSelect(FormWidget):
    def __init__(self, parent):
        self.parent = parent
        
    def widget(self, field, value, **attributes):
        tableId = '%s_%s_cascade' % (field._tablename, field.name)
        wrapper = TABLE(_id = tableId)
        buildSelect(field, value, wrapper)
        return wrapper

def index():
    cascadeWidget=CascadingSelect('parish')
    form = SQLFORM.factory(
        Field('village',
              requires=IS_IN_DB(db, 'village.id', db.village._format),
              widget=cascadeWidget.widget,
              default=3))
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)
