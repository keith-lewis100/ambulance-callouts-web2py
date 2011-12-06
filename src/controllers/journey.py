# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    form = SQLFORM.factory(
        Field('date', 'date'),
        Field('facility', default=session.facility,
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'facility.id',
                                                        db.facility._format))),
        Field('ambulance', default=session.ambulance,
              requires=IS_EMPTY_OR(IS_IN_DB(db, 'ambulance.id',
                                                         db.ambulance._format))))
    if form.process().accepted:
        response.flash = 'form accepted'
        session.date = form.vars.date
        session.facility = form.vars.facility
        session.ambulance = form.vars.ambulance
        redirect(URL('journey.html'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def journey():
    """
return the journey table or edit/create form
    """
    can_modify = auth.has_membership(role='journey_editor')
    query = db.journey.id > 0
    if session.date:
        query = query & (db.journey.call_date == session.date)
        db.journey.call_date.default = session.date
    if session.facility:
        query = query & (db.journey.facility == session.facility)
        db.journey.facility.default = session.facility 
    if session.ambulance:
        query = query & (db.journey.ambulance == session.ambulance)
        db.journey.ambulance.default = session.ambulance
    #Initialize the widget
    add_option = SELECT_OR_ADD_OPTION(form_title="Add new Clinician",
                    controller="journey", function="add_clinician",
                                      button_text = "Add New")
    db.journey.clinician.widget = add_option.widget
    journeys = SQLFORM.grid(query, fields=[db.journey.id, db.journey.call_date, db.journey.hc_time, db.journey.family_name,
                                           db.journey.ambulance, db.journey.condition], create=can_modify, editable=can_modify,
                            deletable=can_modify, csv=False, searchable=False, ui='jquery-ui')
    return dict(journeys=journeys)

def add_clinician():
    #this is the controller function that will appear in our dialog
    form = SQLFORM(db.clinician)

    if form.accepts(request.vars):
        #Then let the user know adding via our widget worked        
        response.flash = T("Added")
        target= request.args[0]
        #close the widget's dialog box
        response.js = '$( "#%s_dialog-form" ).dialog( "close" ); ' %(target)
        #update the options they can select their new category in the main form                
        response.js += """$("#%s").append("<option value='%s'>%s</option>");""" \
                % (target, form.vars.id, form.vars.name)
        #and select the one they just added
        response.js += """$("#%s").val("%s");""" % (target, form.vars.id)
        #finally, return a blank form incase for some reason they wanted to add another option
        return form
    elif form.errors:
        #silly user, just send back the form and it'll still be in our dialog box complete with error messages
        return form
    else:
        #hasn't been submitted yet, just give them the fresh blank form        
        return form
