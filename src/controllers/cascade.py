# -*- coding: utf-8 -*-

def index():
    form = SQLFORM.factory(
        Field('village',
              requires=IS_IN_DB(db, 'village.id', db.village._format)))
    
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)
