from app import db
from app.classes.auth import User
from app.classes.achievements import UserAchievements, whichAch
from app.userdata.views import StatisticsVendor, StatisticsUser

from app.common.functions import floating_decimals
from app.classes.wallet_bch import BchWallet


def profilebar(user_id1, user_id2):
    global user1
    global user1pictureid
    global user1stats
    global user1wallet
    global user1level
    global user1width
    global user1ach
    global user1vendorstats

    global user2
    global user2pictureid
    global user2stats
    global user2wallet
    global user2level
    global user2width
    global user2ach
    global user2vendorstats

    if user_id1:
        user1 = db.session.query(User).filter_by(id=user_id1).first()
        user1getlevel = db.session.query(UserAchievements).filter_by(
            username=user1.username).first()
        user1pictureid = str(user1getlevel.level)
        user1stats = db.session.query(StatisticsUser).filter_by(
            username=user1.username).first()
        user1wallet = db.session.query(
            BchWallet).filter_by(user_id=user1.id).first()
        user1level = db.session.query(UserAchievements).filter_by(
            username=user1.username).first()

        if 1 <= user1level.level <= 3:
            user1widthh = (user1level.experiencepoints / 300)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 4 <= user1level.level <= 7:
            user1widthh = (user1level.experiencepoints / 500)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 8 <= user1level.level <= 10:
            user1widthh = (user1level.experiencepoints / 1000)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 11 <= user1level.level <= 14:
            user1widthh = (user1level.experiencepoints / 1500)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 16 <= user1level.level <= 20:
            user1widthh = (user1level.experiencepoints / 2000)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 21 <= user1level.level <= 25:
            user1widthh = (user1level.experiencepoints / 2250)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 26 <= user1level.level <= 30:
            user1widthh = (user1level.experiencepoints / 5500)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 26 <= user1level.level <= 30:
            user1widthh = (user1level.experiencepoints / 10000)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 26 <= user1level.level <= 30:
            user1widthh = (user1level.experiencepoints / 15000)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 30 <= user1level.level <= 50:
            user1widthh = (user1level.experiencepoints / 20000)*100
            user1width = floating_decimals(user1widthh, 0)
        elif 51 <= user1level.level <= 100:
            user1widthh = (user1level.experiencepoints / 25000)*100
            user1width = floating_decimals(user1widthh, 0)
        else:
            user1widthh = (user1level.experiencepoints / 1000)*100
            user1width = floating_decimals(user1widthh, 0)

        user1ach = db.session.query(whichAch).filter_by(
            user_id=user1.id).first()
        if user1.vendor_account == 1:
            user1vendorstats = db.session.query(
                StatisticsVendor).filter_by(username=user1.username).first()
        else:
            user1vendorstats = 0
    else:
        user1 = 0

    if user_id2 != 0:
        user2 = db.session.query(User).filter_by(id=user_id2).first()
        user2getlevel = db.session.query(UserAchievements).filter_by(
            username=user2.username).first()
        user2pictureid = str(user2getlevel.level)
        user2stats = db.session.query(StatisticsUser).filter_by(
            username=user2.username).first()
        user2wallet = db.session.query(
            BtcWallet).filter_by(user_id=user2.id).first()
        user2level = db.session.query(UserAchievements).filter_by(
            username=user2.username).first()
        user2width = int(user2level.experiencepoints / 10)
        user2ach = db.session.query(whichAch).filter_by(
            user_id=user2.id).first()
        if user2.vendor_account == 1:
            user2vendorstats = db.session.query(
                StatisticsVendor).filter_by(username=user2.username).first()
        else:
            user2vendorstats = 0
    else:
        user2 = 0
        user2getlevel = 0
        user2pictureid = 0
        user2stats = 0
        user2wallet = 0
        user2level = 0
        user2width = 0
        user2ach = 0
        user2vendorstats = 0

    return user1, \
        user1pictureid, \
        user1stats, \
        user1wallet, \
        user1level, \
        user1width, \
        user1ach, \
        user1vendorstats, \
        user2, \
        user2pictureid, \
        user2stats, \
        user2wallet, \
        user2level, \
        user2width, \
        user2ach, \
        user2vendorstats, \
        user2getlevel
