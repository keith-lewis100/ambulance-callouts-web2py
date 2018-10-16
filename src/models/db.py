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

db.define_table('action',
    Field('name', length=80, unique=True, notnull=True),
    format = '%(name)s')

db.define_table('ambulance',
    Field('registration', length=30, unique=True, notnull=True),
    format = '%(registration)s')

db.define_table('condition',
    Field('title', length=80, unique=True, notnull=True),
    format = '%(title)s')

if request.controller != 'appadmin':
    db._common_fields.append(Field('request_tenant',
                                       default='iers.pont-mbale.org.uk',
                                       writable=False))

db.define_table('driver',
    Field('name', length=30, unique=True, notnull=True),
    format = '%(name)s')

db.define_table('facility',
    Field('name', length=30, unique=True, notnull=True),
    Field('stationed_ambulance', 'reference ambulance', ondelete='NO ACTION',
                  requires=IS_EMPTY_OR(IS_IN_DB(db, 'ambulance.id', db.ambulance._format)),
                  represent=lambda id, row: id != None and db.ambulance[id].registration or ''),
    format = '%(name)s')
    
db.define_table('shift',
    Field('station', 'reference facility', ondelete='NO ACTION'),
    Field('ambulance', 'reference ambulance', ondelete='NO ACTION'),
    Field('driver', 'reference driver', ondelete='NO ACTION'),
    Field('date', 'date', notnull=True),
    Field('start_time', 'time', notnull=True),
    Field('end_time', 'time', notnull=True),
    Field('start_mileage', 'integer'),
    Field('end_mileage', 'integer'),
    format = lambda r : '%s on %s at %s' % (r.station.name, r.date, r.start_time))

def location_format(r):
#   if not r.parent:
       return r.name
#   parent = location_format(db.location[r.parent])
#   return '%s/%s' % (parent, r.name)
    
db.define_table('location',
    Field('name', length=30, notnull=True),
    Field('parent', 'reference location'),
    Field('type', 'integer', requires=IS_INT_IN_RANGE(1, 5)),
    format = location_format)

db.location.parent.requires = IS_EMPTY_OR(
                    IS_IN_DB(db, 'location.id', db.location._format))

db.define_table('journey',
    Field('shift', 'reference shift'),
    Field('family_name', length=30, notnull=True),
    Field('given_name', length=30, notnull=True),
    Field('age', 'integer', requires=IS_INT_IN_RANGE(0, 121)),
    Field('sex', requires=IS_IN_SET(['Male','Female']),
          widget=SQLFORM.widgets.radio.widget),
    Field('pregnant', 'boolean', default=False),
    Field('used_stretcher', 'boolean'),
    Field('used_cycle', 'boolean'),
    Field('patient_location', 'reference location', ondelete='NO ACTION',
             requires=IS_EMPTY_OR(IS_IN_DB(db, 'location.id', db.location._format)),
                    represent=lambda id, row:
                        id != None and id != 0 and
                            location_format(db.location[id]) or ''),
    Field('call_time', 'time',
          comment='time of callout'),
    Field('dispatch_time', 'time', required=True,
          comment='time vehicle leaves HC'),
    Field('arrival_time', 'time',
          comment='time vehicle arrives at patient'),
    Field('hc_time', 'time', required=True,
          comment='time patient arrives at facility'),
    Field('condition', 'reference condition', comment='patient condition', ondelete='NO ACTION'),
    Field('amb_action', 'reference action', comment='action by driver', ondelete='NO ACTION',
                requires=IS_EMPTY_OR(IS_IN_DB(db, 'action.id', db.action._format)),
                represent=lambda id, row: id != None and db.action[id].name or ''),
    Field('facility', 'reference facility', ondelete='NO ACTION',
          comment='name of destination HC or Hospital'),
    Field('condition_hc', 'reference condition', comment='patient condition',
                ondelete='NO ACTION',
                requires=IS_EMPTY_OR(IS_IN_DB(db, 'condition.id', db.condition._format)),
                represent=lambda id, row: id != None and db.condition[id].title or ''),   
    Field('notes', 'text'))

