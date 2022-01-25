from app import db
from app.classes.achievements import UserAchievements, UserAchievements_recent
from datetime import datetime

# id = 1
# a1 newbie
def newbie(userid):
    now = datetime.utcnow()
    usera = db.session \
                .query(UserAchievements)\
                .filter_by(userid=userid)\
                .first()
    usera.a1 = 1
    usera.a1_date = now

    addit = UserAchievements_recent(
                                    userid=usera.userid,
                                    username=usera.username,
                                    ach_id=1,
                                    achievement_date=now,
                                    viewed=0,
                                    )
    db.session.add(addit)
    db.session.add(usera)

# id=16
# a2
def Grassisgreeneronmyside(userid):
    now = datetime.utcnow()
    usera = db.session\
            .query(UserAchievements)\
            .filter_by(userid=userid)\
            .first()
    if usera.a2 != 1:
        usera.a2 = 1
        usera.a2_date = now

        addit = UserAchievements_recent(
                                        userid=usera.userid,
                                        username=usera.username,
                                        ach_id=16,
                                        achievement_date=now,
                                        viewed=0,
                                        )
        db.session.add(addit)
        db.session.add(usera)
