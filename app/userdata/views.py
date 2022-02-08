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

from app.achs.c import howmanyitemsbought_customer, howmanytrades_customer
from app.achs.v import howmanyitemssold_vendor, howmanytrades_vendor
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


def addtotalItemsSold(user_id, howmany):
    """
    how many items a customer sold
    """""

    itemssold = db.session\
        .query(StatisticsVendor)\
        .filter(user_id == StatisticsVendor.vendorid)\
        .first()

    a = itemssold.totalsales
    x = int(a) + int(howmany)

    itemssold.totalsales = x

    db.session.add(itemssold)

    howmanyitemssold_vendor(user_id=user_id, number=x)


def addtotalItemsBought(user_id, howmany):
    # how many items a customer bought
    itemsbought = db.session.query(StatisticsUser).filter(
        user_id == StatisticsUser.user_id).first()

    a = itemsbought.totalitemsbought
    x = a + howmany
    itemsbought.totalitemsbought = x

    db.session.add(itemsbought)

    howmanyitemsbought_customer(user_id=user_id, number=x)


def addtotaltradesuser(user_id):
    # how many trades a customer did
    userstats = db.session.query(StatisticsUser).filter(
        user_id == StatisticsUser.user_id).first()
    useramount = userstats.totaltrades
    usernewamount = useramount + 1
    userstats.totaltrades = usernewamount

    db.session.add(userstats)
    db.session.commit()

    # achievement
    howmanytrades_customer(user_id=user_id, number=usernewamount)


def addtotaltradesVendor(user_id):
    # how many trades a customer did
    vendorstats = db.session\
        .query(StatisticsVendor)\
        .filter(user_id == StatisticsVendor.vendorid)\
        .first()
    # add total trades to vendor
    amount = vendorstats.totaltrades
    newamount = amount + 1
    vendorstats.totaltrades = newamount

    db.session.add(vendorstats)

    howmanytrades_vendor(user_id=user_id, number=newamount)


def differenttradingpartners_user(user_id, otherid):
    # adds diff partners to user file
    # get customer txt and write vendor id
    ##
    user = db.session\
        .query(User)\
        .filter(user_id == User.id)\
        .first()
    getuserlocation = userimagelocation(user_id=user_id)
    itemsbought = db.session\
        .query(StatisticsUser)\
        .filter(user_id == StatisticsUser.user_id)\
        .first()
    # find path of the user
    thepath = os.path.join(UPLOADED_FILES_DEST, "user",
                           getuserlocation, str(user_id))
    # make a directory if doesnt have it..should tho
    mkdir_p(path=thepath)
    # text file is user_id
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


def differenttradingpartners_vendor(user_id, otherid):
    """
    # adds diff partners to user file
    # get vendor txt and write customer id
    :param user_id:
    :param otherid:
    :return:
    """
    # get the user
    user = db.session\
        .query(User)\
        .filter(user_id == User.id)\
        .first()
    getuserlocation = userimagelocation(user_id=user_id)
    # get stats if vendor
    itemsbought = db.session\
        .query(StatisticsVendor)\
        .filter(user_id == StatisticsVendor.vendorid)\
        .first()
    # find path of the user

    thepath = os.path.join(UPLOADED_FILES_DEST, "user",
                           getuserlocation, str(user_id))
    # make a directory if doesnt have it..should tho
    mkdir_p(path=thepath)
    # text file is user_id
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


def reviewsgiven(user_id):
    """
    # adds a review given by user
    :param user_id:
    :return:
    """

    reviewsstats = db.session\
        .query(StatisticsUser)\
        .filter(user_id == StatisticsUser.user_id)\
        .first()
    y = reviewsstats.totalreviews
    x = y + 1
    reviewsstats.totalreviews = x

    db.session.add(reviewsstats)


def reviewsrecieved(user_id):
    """
    # adds a review recieved as a vendor
    :param user_id:
    :return:
    """

    reviewsstats = db.session\
        .query(StatisticsVendor)\
        .filter(user_id == StatisticsVendor.vendorid)\
        .first()
    y = reviewsstats.totalreviews
    x = y + 1
    reviewsstats.totalreviews = x

    db.session.add(reviewsstats)


def addflag(user_id):
    # adds a flag to user stats
    reviewsstats = db.session\
        .query(StatisticsUser)\
        .filter(user_id == StatisticsUser.user_id)\
        .first()
    y = reviewsstats.itemsflagged
    x = y + 1
    reviewsstats.itemsflagged = x

    db.session.add(reviewsstats)


def vendorflag(user_id):
    # adds a flag to vendor stats
    vendorstats = db.session\
        .query(StatisticsVendor)\
        .filter(user_id == StatisticsVendor.vendorid)\
        .first()
    # add total trades to vendor
    amount = vendorstats.beenflagged
    newamount = amount + 1
    vendorstats.beenflagged = newamount

    db.session.add(vendorstats)


def totalspentonitems_btccash(user_id, amount, howmany):
    # USER
    # how much money a user has spent of physical items
    # bitcoin cash
    itemsbought = db.session\
        .query(StatisticsUser)\
        .filter(user_id == StatisticsUser.user_id)\
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


def vendortotalmade_btccash(user_id, amount):
    # vendor
    # how much money a user has spent of physical items
    # bitcoin cash
    vendorstats = db.session\
        .query(StatisticsVendor)\
        .filter(user_id == StatisticsVendor.vendorid)\
        .first()
    a = vendorstats.totalbtccashrecieved
    x = (Decimal(a + amount))
    vendorstats.totalbtccashrecieved = x

    # lifetime - calculate usd
    amountinusd = btc_cash_converttolocal(amount=amount, currency=1)
    addmount = vendorstats.totalusdmade + amountinusd
    vendorstats.totalusdmade = addmount

    db.session.add(vendorstats)

# AFFILIATE Stats


def affstats(user_id, amount, currency):

    aff_stats = db.session\
        .query(AffiliateStats)\
        .filter(user_id == AffiliateStats.user_id)\
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


# def totalrecbyusers(user_id, amount, howmany):
#     # how much money a user has spent of physical items
#     # bitcoin
#     itemsbought = db.session.query(StatisticsUser).filter(user_id == StatisticsUser.user_id).first()
#     a = itemsbought.totalbtcrecieved
#     totalamt = (Decimal(amount) * int(howmany))
#     x = (Decimal(a + totalamt))
#     itemsbought.totalbtcrecieved = x
#     db.session.add(itemsbought)
#     db.session.commit()


# def vendortotalsent_btc(user_id, amount):
#     # how much money a user has spent of physical items
#     # bitcoin
#     vendorstats = db.session.query(StatisticsVendor).filter(user_id == StatisticsVendor.vendorid).first()
#     a = vendorstats.totalbtcspent
#     x = (Decimal(a + amount))
#     vendorstats.totalbtcspent = x
#     db.session.add(vendorstats)
#     db.session.commit()


# def totalrecbyusers_btccash(user_id, amount, howmany):
#     # USER
#     # how much money a user has recieved
#     # bitcoin cash
#     itemsbought = db.session.query(StatisticsUser).filter(user_id == StatisticsUser.user_id).first()
#     a = itemsbought.totalbtccashrecieved
#     totalamt = (Decimal(amount) * int(howmany))
#     x = (Decimal(a + totalamt))
#     itemsbought.totalbtccashrecieved = x
#     db.session.add(itemsbought)
#     db.session.commit()


# def vendortotalsent_btccash(user_id, amount):
#     # vendor
#     # how much money a user has spent of physical items
#     # bitcoin cash
#     vendorstats = db.session.query(StatisticsVendor).filter(user_id == StatisticsVendor.vendorid).first()
#     a = vendorstats.totalbtccashspent
#     x = (Decimal(a + amount))
#     vendorstats.totalbtccashspent = x
#     db.session.add(vendorstats)
#     db.session.commit()
