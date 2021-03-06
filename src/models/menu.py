# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('collecting data for PONT')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2011'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default','index'), []),
    (T('Shifts/Journeys'), False, URL('shift', 'index'), []),
    (T('Manage'), False, None, [
           (T('Conditions'), False, URL('manage', 'table', args='condition'), []),
           (T('Actions'), False, URL('manage', 'table', args='action'), []),
           (T('Ambulances'), False, URL('manage', 'table', args='ambulance'), []),
           (T('Drivers'), False, URL('manage', 'table', args='driver'), []),
           (T('Facilities'), False, URL('manage', 'table', args='facility'), []),
           (T('Locations'), False, URL('manage', 'location'), [])]),
    (T('Reports'), True, '', [
           (T('Journeys by condition and month'), False,
                    URL('report', 'index', args='journey_by_condition')),
           (T('Journey Records'), False,
                    URL('report', 'index', args='journey_records'))])
    ]

