from app import db
from app.classes.achievements import UserAchievements, UserAchievements_recent

from datetime import datetime

#id=14
def likemoneyinthebank(userid):
    usera = db.session.query(UserAchievements).filter_by(userid=userid).first()
    now = datetime.utcnow()
    if usera.b1 != 1:
        usera.b1 = 1
        usera.b1_date = now
        addit = UserAchievements_recent(
            userid=usera.userid,
            username=usera.username,
            ach_id=14,
            achievement_date=now,
            viewed=0,
        )
        db.session.add(addit)
        db.session.add(usera)

    else:
        pass

#id=18
def withdrawl(userid):
    usera = db.session.query(UserAchievements).filter_by(userid=userid).first()
    now = datetime.utcnow()
    if usera.b2 != 1:
        usera.b2 = 1
        usera.b2_date = now
        addit = UserAchievements_recent(
            userid=usera.userid,
            username=usera.username,
            ach_id=18,
            achievement_date=now,
            viewed=0,
        )
        db.session.add(addit)
        db.session.add(usera)

    else:
        pass