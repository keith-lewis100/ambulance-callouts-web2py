# -*- coding: utf-8 -*-
from datetime import date, timedelta

@auth.requires_login()
def index():
    # find the last date for a shift
#    max = db.shift.date.max()
#    r = db().select(db.shift.station, max).first()
#    l = r[max] and r[max].strftime('%d %B %Y') or "None"
    l = "None"
    # total journeys entered
    count = db.journey.id.count()
    r = db(db.journey.id > 0).select(count).first()
    total = r[count]  
    # count journeys for the last 30 days
    end_date = date.today();
    start_date = end_date - timedelta(30)
    query = (db.journey.shift == db.shift.id) & \
            (db.shift.date >= start_date) & \
            (db.shift.date <= end_date)
    r = db(query).select(count).first()
    recent = r[count]
    return dict(lastshift=l, total=total, recent=recent)

def user(): return dict(form=auth())
