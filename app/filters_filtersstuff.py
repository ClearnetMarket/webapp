from app import app
from flask import url_for
import os


@app.template_filter('maincatname')
def maincatname(catdid0):
    from app.classes.category import Category_Categories
    from app import db
    if catdid0 == 0:
        nameofcat = 'All Category_Categories'
        return str(nameofcat)
    else:
        thecat = db.session.query(Category_Categories).filter(
            Category_Categories.id == catdid0).first()
        if thecat:
            nameofcat = thecat.name
            return str(nameofcat)
        else:
            nameofcat = ''
            return nameofcat


@app.template_filter('trustlevel')
def trustlevel(userid):
    from app.classes.vendor import Vendor_VendorVerification
    from app import db
    x = db.session.query(Vendor_VendorVerification).filter_by(vendor_id=userid).first()
    if x:
        level = x.vendor_level
        return str(level)
    else:
        level = '0'
        return level


@app.template_filter('marginpercent')
def marginpercent(margin):
    from app.classes.models import Query_Margin
    from app import db
    marginq = db.session.query(Query_Margin).filter_by(id=margin).first()
    return marginq.value


@app.template_filter('buyorsell')
def buyorsell(bors):
    if bors == 1:
        return "Selling"
    else:
        return "Buying"


# gets achievement title
@app.template_filter('achievementtitle')
def achievementtitle(categoryid):
    from app.classes.achievements import Achievements
    from app import db
    getfilter = db.session.query(Achievements).filter_by(
        categoryid=categoryid).first()
    if getfilter:
        return getfilter.title
    else:
        return ""


# gets achievement title
@app.template_filter('achievementdescription')
def achievementdescription(categoryid):
    from app.classes.achievements import Achievements
    from app import db

    getfilter = db.session.query(Achievements).filter_by(
        categoryid=categoryid).first()
    if getfilter:
        return getfilter.description
    else:
        return ""


# converts id to country
@app.template_filter('countryformat')
def countryformat(idofcountry):
    from app.classes.models import Query_Country
    from app import db

    try:
        getcountry = db.session.query(
            Query_Country).filter_by(numericcode=idofcountry).first()
        return getcountry.name
    except Exception:
        name = "World Wide"
        return name

# converts id to country


@app.template_filter('currencyformat')
def currencyformat(id):
    from app.classes.models import Query_Currency
    from app import db

    try:
        getcurrency = db.session.query(
            Query_Currency).filter_by(code=id).first()
        return getcurrency.symbol
    except Exception:
        name = ""
        return name
# get not shipping too name


@app.template_filter('notshippingformat')
def notshippingformat(valueofid):
    from app.classes.models import Query_Continents
    from app import db

    getnotshipping = db.session.query(
        Query_Continents).filter_by(value=valueofid).first()
    if not None:
        return getnotshipping.text
    else:
        return("")

# get not shipping too name


@app.template_filter('returnwhy')
def returnwhy(id):
    from app.classes.models import Query_RequestReturn
    from app import db

    getreturn = db.session.query(Query_RequestReturn).filter_by(id=id).first()
    if not None:
        return getreturn.text
    else:
        return ("")

# get not shipping too name


@app.template_filter('cancelwhy')
def cancelwhy(id):
    from app.classes.models import Query_RequestCancel
    from app import db
    getreturn = db.session.query(Query_RequestCancel).filter_by(id=id).first()
    if not None:
        return getreturn.text
    else:
        return ("")


# Gets how many ratings for the user
@app.template_filter('username')
def username(id):
    from app.classes.auth import Auth_User
    from app import db

    getuser = db.session.query(Auth_User)
    getuser = getuser.filter_by(id=id).first()
    return getuser.username

# Gets how many ratings for the user


@app.template_filter('adminusername')
def adminusername(id):
    from app.classes.auth import Auth_User
    from app import db

    getuser = db.session.query(Auth_User)
    getuser = getuser.filter_by(id=id).first()
    if id == 1:
        return "Escrow"
    elif id == 2:
        return "profit Account"
    else:
        return getuser.username

# Gets how many ratings for the user


@app.template_filter('profilepicture')
def profilepicture(id):
    from app.classes.auth import Auth_User
    from app import db

    user = db.session\
        .query(Auth_User)\
        .filter_by(id=id)\
        .first()

    filenameofprofile = os.path.join(str(user.usernode), str(
        user.id), (user.profileimage + str('_125x.jpg')))

    if user.profileimage == 'user-unknown.png':
        return url_for('userdata.profile_image', filename=('user-unknown.png'))
    else:
        return url_for('userdata.profile_image', filename=(filenameofprofile))


# Gets how many ratings for the user
@app.template_filter('userrating')
def userrating(id):
    from app.classes.profile import Profile_StatisticsUser
    from app import db

    getratings = db.session.query(Profile_StatisticsUser)
    getratings = getratings.filter(Profile_StatisticsUser.user_id == id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.totalreviews


# Gets avg of the ratings for the user
@app.template_filter('avguserrating')
def avguserrating(id):
    from app.classes.profile import Profile_StatisticsUser
    from app import db

    getratings = db.session.query(Profile_StatisticsUser)
    getratings = getratings.filter(Profile_StatisticsUser.user_id == id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.userrating


# Gets how many ratings for the vendor
@app.template_filter('vendorratingcount')
def vendorratingcount(id):
    from app.classes.profile import Profile_StatisticsVendor
    from app import db

    getratings = db.session.query(Profile_StatisticsVendor)
    getratings = getratings.filter(Profile_StatisticsVendor.vendorid == id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.totalreviews


# Gets avg of the ratings for the vendor
@app.template_filter('avgvendorrating')
def avgvendorrating(id):
    from app.classes.profile import Profile_StatisticsVendor
    from app import db

    getratings = db.session.query(Profile_StatisticsVendor)
    getratings = getratings.filter(Profile_StatisticsVendor.vendorid == id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.vendorrating


# Gets avg of the ratings for the vendor
@app.template_filter('vendorratingonorder')
def vendorratingonorder(id):
    from app.classes.userdata import UserData_Feedback
    from app import db
    getratings = db.session.query(UserData_Feedback)
    getratings = getratings.filter(UserData_Feedback.sale_id == id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.vendorrating


@app.template_filter('feedbackcategory')
def feedbackcategory(id):
    from app.classes.models import Query_WebsiteFeedback
    from app import db

    feedback = db.session.query(
        Query_WebsiteFeedback).filter_by(value=id).first()
    return feedback.text


@app.template_filter('lastseen_text')
def lastseen_text(id):
    from app.classes.auth import Auth_User
    from app import db
    user = db.session.query(Auth_User).filter_by(id=id).first()
    lastseen = user.last_seen
    return lastseen


@app.template_filter('lastseen')
def lastseen(id):
    from app.classes.auth import Auth_User
    from datetime import timedelta, datetime
    from app import db

    user = db.session.query(Auth_User).filter_by(id=id).first()
    lastseen = user.last_seen
    now = datetime.utcnow()
    oneminutes = (datetime.utcnow() - timedelta(minutes=1))
    fiveminutes = (datetime.utcnow() - timedelta(minutes=5))
    fifteenminutes = (datetime.utcnow() - timedelta(minutes=15))
    onehour = (datetime.utcnow() - timedelta(hours=1))
    twohalfhour = (datetime.utcnow() - timedelta(hours=2, minutes=30))
    sixhour = (datetime.utcnow() - timedelta(hours=6))
    twelvehour = (datetime.utcnow() - timedelta(hours=12))
    oneday = (datetime.utcnow() - timedelta(hours=24))
    twoday = (datetime.utcnow() - timedelta(days=2))
    week = (datetime.utcnow() - timedelta(days=7))
    month = (datetime.utcnow() - timedelta(days=30))

    if week >= lastseen >= month:
        x = '1'
    elif twoday >= lastseen >= week:
        x = '2'
    elif oneday >= lastseen >= twoday:
        x = '3'
    elif twelvehour >= lastseen >= oneday:
        x = '4'
    elif sixhour >= lastseen >= twelvehour:
        x = '5'
    elif twohalfhour >= lastseen >= sixhour:
        x = '6'
    elif onehour >= lastseen >= twohalfhour:
        x = '7'
    elif fifteenminutes >= lastseen >= onehour:
        x = '8'
    elif fiveminutes >= lastseen >= fifteenminutes:
        x = '9'
    elif oneminutes >= lastseen >= fiveminutes:
        x = '10'
    elif now >= lastseen >= oneminutes:
        x = '11'
    else:
        x = '0'

    return x


# Gets the item count in marketitems subcategory
@app.template_filter('itemsincat')
def itemsincat(subcatid):
    from app.classes.item import Item_MarketItem
    from app import db
    getitems = db.session.query(Item_MarketItem)
    getitems = getitems.filter(Item_MarketItem.subcategory == subcatid)
    getitems = getitems.filter(Item_MarketItem.online == 1)
    item = getitems.count()
    return item


# Gets the item count in marketitems main category
@app.template_filter('itemsincatmain')
def itemsincatmain(id):
    from app.classes.item import Item_MarketItem
    from app import db
    getitems = db.session.query(Item_MarketItem)
    getitems = getitems.filter(Item_MarketItem.category == id)
    getitems = getitems.filter(Item_MarketItem.online == 1)
    item = getitems.count()
    return item

# Gets the item count in marketitems main category


@app.template_filter('carrierformat')
def carrierformat(id):
    from app.classes.models import Query_Carriers
    from app import db
    getitems = db.session.query(Query_Carriers)
    getitems = getitems.filter(Query_Carriers.value == id).first()
    item = getitems.text
    return item


# Gets an item picture if exists..else returns default image
@app.template_filter('orderpicture')
def orderpicture(itemid, type):
    from app.classes.item import Item_MarketItem
    from app import db
    # <img src="{{ order.trade_id|orderpicture(type=2) }}" width="200px" height="200px">
    # <img src="{{ order.item_id|orderpicture(type=1) }}" width="200px" height="200px">

    if type == 1:
        x = db.session.query(Item_MarketItem).filter(
            itemid == Item_MarketItem.id).first()
        if x == None:
            # give default image
            return url_for('static', filename='/images/Noimage.png')
        else:
            if x.image_one == '0':
                return url_for('static', filename='/images/Noimage.png')
            else:
                # get primary image
                return url_for('userdata.media_file', nodeid=x.string_node_id, filename=(x.string + x.image_one))
    elif type == 2:
        pass

    elif type == 3:
        pass
    else:
        pass


@app.template_filter('usdtocurrency')
def usdtocurrency(price, currency):
    from app.classes.wallet_bch import Bch_Prices
    from app import db
    from decimal import Decimal
    getcurrentprice = db.session.query(
        Bch_Prices).filter_by(currency_id=currency).first()
    if currency == 0:
        return price
    else:
        x = Decimal(price) / Decimal(getcurrentprice.price)
        bt = (Decimal(getcurrentprice.price) * x)
        c = '{0:.2f}'.format(bt)
        return c
