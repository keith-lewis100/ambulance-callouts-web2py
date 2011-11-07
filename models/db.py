# -*- coding: utf-8 -*-
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

if not request.env.web2py_runtime_gae:     
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite') 
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore') 
    ## store sessions and tickets there
    session.connect(request, response, db = db) 
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth
auth = Auth(db, hmac_key=Auth.get_or_create_key()) 

## create all tables needed by auth if not custom tables
auth.define_tables() 

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.reset_password_requires_verification = True
auth.settings.actions_disabled.append('register')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('ambulance',
    Field('name', length=120),
    Field('registration', length=120),
    format = '%(name)s')

db.define_table('facility',
    Field('name', length=120),
    format = '%(name)s')
    
db.define_table('condition',
    Field('title', length=120),
    format = '%(title)s')

db.define_table('clinician',
    Field('name', length=120),
    format = '%(name)s')

db.define_table('driver',
    Field('name', length=120),
    format = '%(name)s')

db.define_table('shift',
    Field('ambulance', 'reference ambulance'),
    Field('driver', 'reference driver'),
    Field('start_time', 'datetime', required=True),
    Field('start_mileage', 'integer'),
    Field('end_mileage', 'integer'),
    format = '%(ambulance.name)s on %(start_time)s')

db.define_table('journey',
    Field('ambulance', 'reference ambulance'),
    Field('family_name', length=30, required=True),
    Field('given_name', length=30, required=True),
    Field('start_location', length=30),
    Field('call_time', 'datetime', required=True),
    Field('arrival_time', 'datetime', required=False),
    Field('end_time', 'datetime', required=False),
    Field('condition', 'reference condition'),
    Field('facility', 'reference facility'),
    Field('action', length=120),
    Field('outcome', length=120),
    Field('clinician', 'reference clinician',
      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clinician.id', db.clinician._format))))


