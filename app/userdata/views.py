import os
from app.userdata import userdata
from app import UPLOADED_FILES_DEST
from flask import send_from_directory
from app import db
# models
from app.classes.auth import User

from app.classes.profile import \
    StatisticsUser, \
    StatisticsVendor

from app.classes.affiliate import \
    AffiliateStats

# End Models
from app.achievements.c import howmanyitemsbought_customer, howmanytrades_customer
from app.achievements.v import howmanyitemssold_vendor, howmanytrades_vendor
from app.common.functions import mkdir_p,  btc_cash_converttolocal, userimagelocation
from datetime import datetime
from decimal import Decimal

now = datetime.utcnow()

@userdata.route('/item/<path:filename>')
def media_file(filename):

    return send_from_directory(UPLOADED_FILES_DEST, filename, as_attachment=False)


@userdata.route('/user/<path:filename>')
def profile_image(filename):

    return send_from_directory(UPLOADED_FILES_DEST, filename, as_attachment=False)


def addtotalItemsSold(userid, howmany):
    """
    how many items a customer sold
    """""

    itemssold = db.session\
    .query(StatisticsVendor)\
    .filter(userid == StatisticsVendor.vendorid)\
    .first()

    a = itemssold.totalsales
    x = int(a) + int(howmany)

    itemssold.totalsales = x

    db.session.add(itemssold)

    howmanyitemssold_vendor(userid=userid, number=x)



def addtotalItemsBought(userid, howmany):
    # how many items a customer bought
    itemsbought = db.session.query(StatisticsUser).filter(userid == StatisticsUser.usernameid).first()

    a = itemsbought.totalitemsbought
    x = a + howmany
    itemsbought.totalitemsbought = x

    db.session.add(itemsbought)
  

    howmanyitemsbought_customer(userid=userid, number=x)



def addtotaltradesuser(userid):
    # how many trades a customer did
    userstats = db.session.query(StatisticsUser).filter(userid == StatisticsUser.usernameid).first()
    useramount = userstats.totaltrades
    usernewamount = useramount + 1
    userstats.totaltrades = usernewamount

    db.session.add(userstats)
    db.session.commit()

    # achievement
    howmanytrades_customer(userid=userid, number=usernewamount)


def addtotaltradesVendor(userid):
    # how many trades a customer did
    vendorstats = db.session\
    .query(StatisticsVendor)\
    .filter(userid == StatisticsVendor.vendorid)\
    .first()
    # add total trades to vendor
    amount = vendorstats.totaltrades
    newamount = amount + 1
    vendorstats.totaltrades = newamount

    db.session.add(vendorstats)


    howmanytrades_vendor(userid=userid, number=newamount)



def differenttradingpartners_user(userid, otherid):
    # adds diff partners to user file
    # get customer txt and write vendor id
    ##
    user = db.session\
    .query(User)\
    .filter(userid == User.id)\
    .first()
    getuserlocation = userimagelocation(userid=userid)
    itemsbought = db.session\
    .query(StatisticsUser)\
    .filter(userid == StatisticsUser.usernameid)\
    .first()
    # find path of the user
    thepath = os.path.join(UPLOADED_FILES_DEST, "user", getuserlocation, str(userid))
    # make a directory if doesnt have it..should tho
    mkdir_p(path=thepath)
    # text file is userid
    usertextfile = str(user.id) + ".txt"
    # text file location
    userfile = os.path.join(thepath, usertextfile)
    # vendor trade log
    othertraderid = str(otherid)
    text_file = open(userfile, "a")
    f = open(userfile, 'r')
    x = set(f.read().split(','))
    if str(otherid) in x:
        y = (len(x)) - 1
        itemsbought.diffpartners = y
    else:
        text_file.write(othertraderid + ',')
        text_file.close()
        y = (len(x))
        itemsbought.diffpartners = y

    db.session.add(itemsbought) 



def differenttradingpartners_vendor(userid, otherid):
    """
    # adds diff partners to user file
    # get vendor txt and write customer id
    :param userid:
    :param otherid:
    :return:
    """
    # get the user
    user = db.session\
    .query(User)\
    .filter(userid == User.id)\
    .first()
    getuserlocation = userimagelocation(userid=userid)
    # get stats if vendor
    itemsbought = db.session\
    .query(StatisticsVendor)\
    .filter(userid == StatisticsVendor.vendorid)\
    .first()
    # find path of the user

    thepath = os.path.join(UPLOADED_FILES_DEST, "user", getuserlocation, str(userid))
    # make a directory if doesnt have it..should tho
    mkdir_p(path=thepath)
    # text file is userid
    usertextfile = str(user.id) + ".txt"
    # text file location
    userfile = os.path.join(thepath, usertextfile)
    # get the other persons id
    othertraderid = str(otherid)
    text_file = open(userfile, "a")
    f = open(userfile, 'r')
    x = set(f.read().split(','))
    if str(otherid) in x:
        y = (len(x)) - 1
        itemsbought.diffpartners = y
    else:
        text_file.write(othertraderid + ',')
        text_file.close()
        y = (len(x))
        itemsbought.diffpartners = y

    db.session.add(itemsbought)



def reviewsgiven(userid):
    """
    # adds a review given by user
    :param userid:
    :return:
    """

    reviewsstats = db.session\
    .query(StatisticsUser)\
    .filter(userid == StatisticsUser.usernameid)\
    .first()
    y = reviewsstats.totalreviews
    x = y + 1
    reviewsstats.totalreviews = x

    db.session.add(reviewsstats)

def reviewsrecieved(userid):
    """
    # adds a review recieved as a vendor
    :param userid:
    :return:
    """

    reviewsstats = db.session\
    .query(StatisticsVendor)\
    .filter(userid == StatisticsVendor.vendorid)\
    .first()
    y = reviewsstats.totalreviews
    x = y + 1
    reviewsstats.totalreviews = x

    db.session.add(reviewsstats)


def addflag(userid):
    # adds a flag to user stats
    reviewsstats = db.session\
    .query(StatisticsUser)\
    .filter(userid == StatisticsUser.usernameid)\
    .first()
    y = reviewsstats.itemsflagged
    x = y + 1
    reviewsstats.itemsflagged = x

    db.session.add(reviewsstats)



def vendorflag(userid):
    # adds a flag to vendor stats
    vendorstats = db.session\
    .query(StatisticsVendor)\
    .filter(userid == StatisticsVendor.vendorid)\
    .first()
    # add total trades to vendor
    amount = vendorstats.beenflagged
    newamount = amount + 1
    vendorstats.beenflagged = newamount

    db.session.add(vendorstats)



def totalspentonitems_btccash(userid, amount, howmany):
    # USER
    # how much money a user has spent of physical items
    # bitcoin cash
    itemsbought = db.session\
    .query(StatisticsUser)\
    .filter(userid == StatisticsUser.usernameid)\
    .first()
    a = itemsbought.totalbtccashspent
    totalamt = (Decimal(amount) * int(howmany))
    x = (Decimal(a + totalamt))
    itemsbought.totalbtccashspent = x

    # lifetime - calculate usd
    amountinusd = btc_cash_converttolocal(amount=amount, currency=1)
    addmount = itemsbought.totalusdspent + amountinusd
    itemsbought.totalusdspent = addmount

    db.session.add(itemsbought)


def vendortotalmade_btccash(userid, amount):
    # vendor
    # how much money a user has spent of physical items
    # bitcoin cash
    vendorstats = db.session\
    .query(StatisticsVendor)\
    .filter(userid == StatisticsVendor.vendorid)\
    .first()
    a = vendorstats.totalbtccashrecieved
    x = (Decimal(a + amount))
    vendorstats.totalbtccashrecieved = x

    # lifetime - calculate usd
    amountinusd = btc_cash_converttolocal(amount=amount, currency=1)
    addmount = vendorstats.totalusdmade + amountinusd
    vendorstats.totalusdmade = addmount

    db.session.add(vendorstats)





# def totalrecbyusers(userid, amount, howmany):
#     # how much money a user has spent of physical items
#     # bitcoin
#     itemsbought = db.session.query(StatisticsUser).filter(userid == StatisticsUser.usernameid).first()
#     a = itemsbought.totalbtcrecieved
#     totalamt = (Decimal(amount) * int(howmany))
#     x = (Decimal(a + totalamt))
#     itemsbought.totalbtcrecieved = x
#     db.session.add(itemsbought)
#     db.session.commit()


# def vendortotalsent_btc(userid, amount):
#     # how much money a user has spent of physical items
#     # bitcoin
#     vendorstats = db.session.query(StatisticsVendor).filter(userid == StatisticsVendor.vendorid).first()
#     a = vendorstats.totalbtcspent
#     x = (Decimal(a + amount))
#     vendorstats.totalbtcspent = x
#     db.session.add(vendorstats)
#     db.session.commit()



# def totalrecbyusers_btccash(userid, amount, howmany):
#     # USER
#     # how much money a user has recieved
#     # bitcoin cash
#     itemsbought = db.session.query(StatisticsUser).filter(userid == StatisticsUser.usernameid).first()
#     a = itemsbought.totalbtccashrecieved
#     totalamt = (Decimal(amount) * int(howmany))
#     x = (Decimal(a + totalamt))
#     itemsbought.totalbtccashrecieved = x
#     db.session.add(itemsbought)
#     db.session.commit()


# def vendortotalsent_btccash(userid, amount):
#     # vendor
#     # how much money a user has spent of physical items
#     # bitcoin cash
#     vendorstats = db.session.query(StatisticsVendor).filter(userid == StatisticsVendor.vendorid).first()
#     a = vendorstats.totalbtccashspent
#     x = (Decimal(a + amount))
#     vendorstats.totalbtccashspent = x
#     db.session.add(vendorstats)
#     db.session.commit()


# AFFILIATE Stats
def affstats(userid, amount, currency):

    aff_stats = db.session\
    .query(AffiliateStats)\
    .filter(userid == AffiliateStats.userid)\
    .first()

    totalorders = aff_stats.totalitemsordered + 1

    aff_stats.totalitemsordered = totalorders
    aff_stats.promoenteredcount = totalorders

    if currency == 2:
        newamount = aff_stats.btc_earned + amount
        aff_stats.btc_earned = newamount

    else:
        newamount = aff_stats.btc_cash_earned + amount
        aff_stats.btc_cash_earned = newamount

    db.session.add(aff_stats)
