import os
from app.userdata import userdata
from app import UPLOADED_FILES_DEST_ITEM, UPLOADED_FILES_DEST_USER
from flask import send_from_directory
from app import db

from decimal import Decimal
# models
from app.classes.auth import Auth_User
from datetime import datetime

from app.classes.profile import \
    Profile_StatisticsUser, \
    Profile_StatisticsVendor

from app.classes.affiliate import Affiliate_Stats

# End Models
from app.achs.c import howmanyitemsbought_customer, howmanytrades_customer
from app.achs.v import howmanyitemssold_vendor, howmanytrades_vendor
from app.common.functions import mkdir_p,  convert_to_local_bch, userimagelocation

now = datetime.utcnow()


@userdata.route('/item/<path:filename>')
def media_file(filename):
    """Function is for returning item images

    Args:
        filename ([type]): [description]

    Returns:
        returns url link
    """
   
    
    return send_from_directory(UPLOADED_FILES_DEST_ITEM, filename, as_attachment=False)


@userdata.route('/user/<path:filename>')
def profile_image(filename):

    return send_from_directory(UPLOADED_FILES_DEST_USER, filename, as_attachment=False)


def addtotalItemsSold(user_id, howmany):
    """
    how many items a customer sold
    """""

    itemssold = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendorid)\
        .first()

    a = itemssold.totalsales
    x = int(a) + int(howmany)

    itemssold.totalsales = x

    db.session.add(itemssold)

    howmanyitemssold_vendor(user_id=user_id, number=x)


def userdata_add_total_items_bought(user_id, howmany):
    # how many items a customer bought
    itemsbought = db.session.query(Profile_StatisticsUser).filter(
        user_id == Profile_StatisticsUser.user_id).first()

    a = itemsbought.totalitemsbought
    x = a + howmany
    itemsbought.totalitemsbought = x

    db.session.add(itemsbought)

    howmanyitemsbought_customer(user_id=user_id, number=x)


def userdata_add_total_trades_user(user_id):
    # how many trades a customer did
    userstats = db.session.query(Profile_StatisticsUser).filter(
        user_id == Profile_StatisticsUser.user_id).first()
    useramount = userstats.totaltrades
    usernewamount = useramount + 1
    userstats.totaltrades = usernewamount

    db.session.add(userstats)
    db.session.commit()

    # achievement
    howmanytrades_customer(user_id=user_id, number=usernewamount)


def userdata_add_total_trades_vendor(user_id):
    # how many trades a customer did
    vendorstats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendorid)\
        .first()
    # add total trades to vendor
    amount = vendorstats.totaltrades
    newamount = amount + 1
    vendorstats.totaltrades = newamount

    db.session.add(vendorstats)

    howmanytrades_vendor(user_id=user_id, number=newamount)


def userdata_different_trading_partners_user(user_id, otherid):
    # adds diff partners to user file
    # get customer txt and write vendor id
    ##
    user = db.session\
        .query(Auth_User)\
        .filter(user_id == Auth_User.id)\
        .first()
    getuserlocation = userimagelocation(user_id=user_id)
    itemsbought = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_id)\
        .first()
    # find path of the user
    thepath = os.path.join(UPLOADED_FILES_DEST_USER,
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


def userdata_different_trading_partners_vendor(user_id, otherid):
    """
    # adds diff partners to user file
    # get vendor txt and write customer id
    :param user_id:
    :param otherid:
    :return:
    """
    # get the user
    user = db.session\
        .query(Auth_User)\
        .filter(user_id == Auth_User.id)\
        .first()
    getuserlocation = userimagelocation(user_id=user_id)
    # get stats if vendor
    itemsbought = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendorid)\
        .first()
    # find path of the user

    thepath = os.path.join(UPLOADED_FILES_DEST_USER,
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


def userdata_reviews_given(user_id):
    """
    # adds a review given by user
    :param user_id:
    :return:
    """

    reviewsstats = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_id)\
        .first()
    y = reviewsstats.totalreviews
    x = y + 1
    reviewsstats.totalreviews = x

    db.session.add(reviewsstats)


def userdata_reviews_recieved(user_id):
    """
    # adds a review recieved as a vendor
    :param user_id:
    :return:
    """

    reviewsstats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendorid)\
        .first()
    y = reviewsstats.totalreviews
    x = y + 1
    reviewsstats.totalreviews = x

    db.session.add(reviewsstats)


def userdata_add_flag(user_id):
    # adds a flag to user stats
    reviewsstats = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_id)\
        .first()
    y = reviewsstats.itemsflagged
    x = y + 1
    reviewsstats.itemsflagged = x

    db.session.add(reviewsstats)


def userdata_vendor_flag(user_id):
    # adds a flag to vendor stats
    vendorstats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendorid)\
        .first()
    # add total trades to vendor
    amount = vendorstats.beenflagged
    newamount = amount + 1
    vendorstats.beenflagged = newamount

    db.session.add(vendorstats)


def userdata_total_spent_on_item_bch(user_id, amount, howmany):
    # USER
    # how much money a user has spent of physical items
    # bitcoin cash
    itemsbought = db.session\
        .query(Profile_StatisticsUser)\
        .filter(user_id == Profile_StatisticsUser.user_id)\
        .first()
    a = itemsbought.totalbtccashspent
    totalamt = (Decimal(amount) * int(howmany))
    x = (Decimal(a + totalamt))
    itemsbought.totalbtccashspent = x

    # lifetime - calculate usd
    amountinusd = convert_to_local_bch(amount=amount, currency=1)
    addmount = itemsbought.totalusdspent + amountinusd
    itemsbought.totalusdspent = addmount

    db.session.add(itemsbought)


def userdata_total_made_on_item_bch(user_id, amount):
    # vendor
    # how much money a user has spent of physical items
    # bitcoin cash
    vendorstats = db.session\
        .query(Profile_StatisticsVendor)\
        .filter(user_id == Profile_StatisticsVendor.vendorid)\
        .first()
    a = vendorstats.totalbtccashrecieved
    x = (Decimal(a + amount))
    vendorstats.totalbtccashrecieved = x

    # lifetime - calculate usd
    amountinusd = convert_to_local_bch(amount=amount, currency=1)
    addmount = vendorstats.totalusdmade + amountinusd
    vendorstats.totalusdmade = addmount

    db.session.add(vendorstats)

# AFFILIATE Stats


def userdata_aff_stats(user_id, amount, currency):

    aff_stats = db.session\
        .query(Affiliate_Stats)\
        .filter(user_id == Affiliate_Stats.user_id)\
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
#     itemsbought = db.session.query(Profile_StatisticsUser).filter(user_id == Profile_StatisticsUser.user_id).first()
#     a = itemsbought.totalbtcrecieved
#     totalamt = (Decimal(amount) * int(howmany))
#     x = (Decimal(a + totalamt))
#     itemsbought.totalbtcrecieved = x
#     db.session.add(itemsbought)
#     db.session.commit()


# def vendortotalsent_btc(user_id, amount):
#     # how much money a user has spent of physical items
#     # bitcoin
#     vendorstats = db.session.query(Profile_StatisticsVendor).filter(user_id == Profile_StatisticsVendor.vendorid).first()
#     a = vendorstats.totalbtcspent
#     x = (Decimal(a + amount))
#     vendorstats.totalbtcspent = x
#     db.session.add(vendorstats)
#     db.session.commit()


# def totalrecbyusers_btccash(user_id, amount, howmany):
#     # USER
#     # how much money a user has recieved
#     # bitcoin cash
#     itemsbought = db.session.query(Profile_StatisticsUser).filter(user_id == Profile_StatisticsUser.user_id).first()
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
#     vendorstats = db.session.query(Profile_StatisticsVendor).filter(user_id == Profile_StatisticsVendor.vendorid).first()
#     a = vendorstats.totalbtccashspent
#     x = (Decimal(a + amount))
#     vendorstats.totalbtccashspent = x
#     db.session.add(vendorstats)
#     db.session.commit()
