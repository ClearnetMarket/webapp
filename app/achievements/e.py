from app import db
from app.classes.achievements import UserAchievements, UserAchievements_recent
from app.classes.auth import User
from datetime import datetime


##e-X level awards
def levelawards(userid):
    now = datetime.utcnow()
    user = db.session.query(User).filter_by(id=userid).first()
    usera = db.session.query(UserAchievements).filter_by(userid=userid).first()
    if usera.level == 2:
        if usera.e1 != 1:
            # id = 4
            #give user some admin roles
            usera.e1 = 1
            usera.e1_date = now

            addit = UserAchievements_recent(
                userid=usera.userid,
                username=usera.username,
                ach_id=4,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    elif usera.level == 5:
        if usera.e2 != 1:
            # id = 2
            usera.e2 = 1
            usera.e2_date = now
            user.admin_role = 1
            addit = UserAchievements_recent(
                userid=usera.userid,
                username=usera.username,
                ach_id=2,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(user)
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    elif usera.level == 10:
        if usera.e3 != 1:
            # id = 3
            usera.e3 = 1
            usera.e3_date = now
            addit = UserAchievements_recent(
                userid=usera.userid,
                username=usera.username,
                ach_id=3,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)
        else:
            pass
    elif usera.level == 25:
        if usera.e4 != 1:
            # id = 5
            usera.e4 = 1
            usera.e4_date = now
            addit = UserAchievements_recent(
                userid=usera.userid,
                username=usera.username,
                ach_id=5,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass

    elif usera.level == 50:
        if usera.e5 != 1:
            # id = 6
            usera.e5 = 1
            usera.e5_date = now
            addit = UserAchievements_recent(
                userid=usera.userid,
                username=usera.username,
                ach_id=6,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass

    elif usera.level == 100:
        if usera.e6 != 1:
            # id = 7
            usera.e6 = 1
            usera.e6_date = now
            addit = UserAchievements_recent(
                userid=usera.userid,
                username=usera.username,
                ach_id=7,
                achievement_date=now,
                viewed=0,
            )
            db.session.add(addit)
            db.session.add(usera)

        else:
            pass
    else:
        pass


