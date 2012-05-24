# -*- coding: utf-8 -*-
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

if not request.env.web2py_runtime_gae:     
    ## if NOT running on Google App Engine use SQLite or other DB
#    db = DAL('postgres://user:password@localhost:5432/iersdb')
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
    Field('name', length=30, unique=True, notnull=True),
    Field('registration', length=120, notnull=True),
    format = '%(name)s')

db.define_table('facility',
    Field('name', length=30, unique=True, notnull=True),
    format = '%(name)s')
    
db.define_table('condition',
    Field('title', length=80, unique=True, notnull=True),
    format = '%(title)s')

#db.define_table('clinician',
#    Field('name', length=80, unique=True, notnull=True),
#    format = '%(name)s')

db.define_table('driver',
    Field('name', length=80, unique=True, notnull=True),
    format = '%(name)s')

db.define_table('action',
    Field('name', length=80, unique=True, notnull=True),
    format = '%(name)s')

db.define_table('district',
    Field('name', length=30, unique=True, notnull=True),
    format = '%(name)s')

db.define_table('subCounty',
    Field('name', length=30, notnull=True),
    Field('district', 'reference district'),
    format = lambda r: (r.district, r.name))

db.define_table('parish',
    Field('name', length=30, notnull=True),
    Field('subCounty', 'reference subCounty'),
    format = lambda r: (r.subCounty, r.name))

db.define_table('village',
    Field('name', length=30, notnull=True),
    Field('parish', 'reference parish'),
    format = lambda r: (r.parish, r.name))

db.define_table('shift',
    Field('ambulance', 'reference ambulance'),
    Field('driver', 'reference driver'),
    Field('date', 'date', notnull=True),
    Field('start_time', 'time', notnull=True),
    Field('end_time', 'time', notnull=True),
    Field('start_mileage', 'integer'),
    Field('end_mileage', 'integer'),
    format = lambda r : '%s on %s at %s' % (r.ambulance.name, r.date, r.start_time))

db.define_table('journey',
    Field('shift', 'reference shift'),
    Field('family_name', length=30, notnull=True),
    Field('given_name', length=30, notnull=True),
    Field('age', 'integer', requires=IS_INT_IN_RANGE(0, 121), notnull=True),
    Field('sex', requires=IS_IN_SET(['Male','Female']), widget=SQLFORM.widgets.radio.widget,
                 notnull=True),
    Field('maternity', 'boolean', default=False, notnull=True),
#    Field('start_location', length=30),
    Field('call_time', 'time', comment='time of callout'),
    Field('dispatch_time', 'time', comment='time vehicle leaves HC'),
    Field('arrival_time', 'time', comment='time vehicle arrives at patient'),
    Field('hc_time', 'time', notnull=True, comment='time patient arrives at facility'),
    Field('condition', 'reference condition', comment='patient condition'),
    Field('amb_action', 'reference action', comment='action by driver',
                requires=IS_EMPTY_OR(IS_IN_DB(db, 'action.id', db.action._format))),
    Field('facility', 'reference facility', comment='name of HC or Hospital'),
#    Field('hc_action', length=120, comment='action at HC'),
    Field('outcome', length=120),
#    Field('clinician', 'reference clinician', comment='person in attendance at HC',
#                requires=IS_EMPTY_OR(IS_IN_DB(db, 'clinician.id', db.clinician._format))),
    Field('notes', 'text'))
