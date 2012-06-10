# -*- coding: utf-8 -*-

from widgets import CascadingSelect

def index():
    cascadeWidget=CascadingSelect(4, db.location.type)
    form = SQLFORM.factory(
        Field('village',
              requires=IS_IN_DB(db, 'location.id', db.location._format),
              widget=cascadeWidget.widget,
              default=None))
    if form.process().accepted:
        response.flash = 'form accepted val = ' + form.vars.village
    elif form.errors:
        response.flash = 'form has errors'
    response.files.append(URL('static', 'js/cascade.js'))
    return dict(form=form)

def dummy():
    return dict()
