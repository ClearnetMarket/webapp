from app import app
from flask import url_for
import os


@app.template_filter('maincatname')
def maincatname(catdid0):
    from app.classes.item import Categories
    from app import db
    if catdid0 == 0:
        nameofcat = 'All Categories'
        return str(nameofcat)
    else:
        thecat = db.session.query(Categories).filter(Categories.id == catdid0).first()
        if thecat:
            nameofcat = thecat.name
            return str(nameofcat)
        else:
            nameofcat = ''
            return nameofcat


@app.template_filter('trustlevel')
def trustlevel(id):
    from app.classes.vendor import vendorVerification
    from app import db
    x = db.session.query(vendorVerification).filter_by(vendor_id=id).first()
    if x:
        level = x.vendor_level
        return str(level)
    else:
        level = '0'
        return level


@app.template_filter('marginpercent')
def marginpercent(margin):
    from app.classes.models import Query_margin
    from app import db
    marginq = db.session.query(Query_margin).filter_by(id=margin).first()
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
    getfilter = db.session.query(Achievements).filter_by(categoryid=categoryid).first()
    if getfilter:
        return getfilter.title
    else:
        return ""



# gets achievement title
@app.template_filter('achievementdescription')
def achievementdescription(categoryid):
    from app.classes.achievements import Achievements
    from app import db

    getfilter = db.session.query(Achievements).filter_by(categoryid=categoryid).first()
    if getfilter:
        return getfilter.description
    else:
        return ""


# converts id to country
@app.template_filter('countryformat')
def countryformat(id):
    from app.classes.models import Country
    from app import db

    try:
        getcountry = db.session.query(Country).filter_by(numericcode=id).first()
        return getcountry.name
    except Exception:
        name = "World Wide"
        return name

# get not shipping too name
@app.template_filter('notshippingformat')
def notshippingformat(id):
    from app.classes.models import Query_Continents
    from app import db

    getnotshipping = db.session.query(Query_Continents).filter_by(value=id).first()
    if not None:
        return getnotshipping.text
    else:
        return("")

# get not shipping too name
@app.template_filter('returnwhy')
def returnwhy(id):
    from app.classes.models import Query_requestreturn
    from app import db

    getreturn = db.session.query(Query_requestreturn).filter_by(id=id).first()
    if not None:
        return getreturn.text
    else:
        return ("")

# get not shipping too name
@app.template_filter('cancelwhy')
def cancelwhy(id):
    from app.classes.models import Query_requestcancel
    from app import db
    getreturn = db.session.query(Query_requestcancel).filter_by(id=id).first()
    if not None:
        return  getreturn.text
    else:
        return ("")


# Gets how many ratings for the user
@app.template_filter('username')
def username(id):
    from app.classes.auth import User
    from app import db

    getuser = db.session.query(User)
    getuser = getuser.filter_by(id=id).first()
    return getuser.username

# Gets how many ratings for the user
@app.template_filter('adminusername')
def adminusername(id):
    from app.classes.auth import User
    from app import db

    getuser = db.session.query(User)
    getuser = getuser.filter_by(id=id).first()
    if id == 1:
        return "Escrow"
    elif id ==2:
        return "profit Account"
    else:
        return getuser.username

# Gets how many ratings for the user
@app.template_filter('profilepicture')
def profilepicture(id):
    from app.classes.auth import User
    from app import db

    user = db.session.query(User)
    user = user.filter_by(id=id).first()
    import platform
    x = (platform.system())
    if x == 'Windows':
        useridlocation = str(user.id) + '/'
        filenameofprofile = os.path.join('user/', '1/', str(useridlocation), user.profileimage)
    else:
        filenameofprofile = os.path.join('user', '1', str(user.id), user.profileimage)

    if user.profileimage == 'user-unknown.png':
        return url_for('userdata.profile_image', filename=('user/' + 'user-unknown.png'))
    elif user.profileimage == '0':
        return url_for('userdata.profile_image', filename=('user/' + 'user-unknown.png'))
    else:
        return url_for('userdata.profile_image', filename=(filenameofprofile))


# Gets how many ratings for the user
@app.template_filter('userrating')
def userrating(id):
    from app.classes.profile import StatisticsUser
    from app import db

    getratings = db.session.query(StatisticsUser)
    getratings = getratings.filter(StatisticsUser.usernameid == id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.totalreviews



# Gets avg of the ratings for the user
@app.template_filter('avguserrating')
def avguserrating(id):
    from app.classes.profile import StatisticsUser
    from app import db

    getratings = db.session.query(StatisticsUser)
    getratings = getratings.filter(StatisticsUser.usernameid==id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.userrating


# Gets how many ratings for the vendor
@app.template_filter('vendorratingcount')
def vendorratingcount(id):
    from app.classes.profile import StatisticsVendor
    from app import db

    getratings = db.session.query(StatisticsVendor)
    getratings = getratings.filter(StatisticsVendor.vendorid==id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.totalreviews


# Gets avg of the ratings for the vendor
@app.template_filter('avgvendorrating')
def avgvendorrating(id):
    from app.classes.profile import StatisticsVendor
    from app import db

    getratings = db.session.query(StatisticsVendor)
    getratings = getratings.filter(StatisticsVendor.vendorid==id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.vendorrating


# Gets avg of the ratings for the vendor
@app.template_filter('vendorratingonorder')
def vendorratingonorder(id):
    from app.classes.userdata import Feedback
    from app import db
    getratings = db.session.query(Feedback)
    getratings = getratings.filter(Feedback.sale_id == id)
    rate = getratings.first()
    if rate is None:
        return 0
    else:
        return rate.vendorrating


@app.template_filter('feedbackcategory')
def feedbackcategory(id):
    from app.classes.models import Query_websitefeedback
    from app import db

    feedback = db.session.query(Query_websitefeedback).filter_by(value=id).first()
    return feedback.text


@app.template_filter('lastseen_text')
def lastseen_text(id):
    from app.classes.auth import User
    from app import db
    user = db.session.query(User).filter_by(id=id).first()
    lastseen = user.last_seen
    return lastseen


@app.template_filter('lastseen')
def lastseen(id):
    from app.classes.auth import User
    from datetime import timedelta, datetime
    from app import db

    user = db.session.query(User).filter_by(id=id).first()
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
    from app.classes.item import marketItem
    from app import db
    getitems = db.session.query(marketItem)
    getitems = getitems.filter(marketItem.subcategory == subcatid)
    getitems = getitems.filter(marketItem.online == 1)
    item = getitems.count()
    return item


# Gets the item count in marketitems main category
@app.template_filter('itemsincatmain')
def itemsincatmain(id):
    from app.classes.item import marketItem
    from app import db
    getitems = db.session.query(marketItem)
    getitems = getitems.filter(marketItem.category == id)
    getitems = getitems.filter(marketItem.online == 1)
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
    from app.classes.item import marketItem
    from app import db
    # <img src="{{ order.trade_id|orderpicture(type=2) }}" width="200px" height="200px">
    # <img src="{{ order.item_id|orderpicture(type=1) }}" width="200px" height="200px">

    if type == 1:
        x = db.session.query(marketItem).filter(itemid == marketItem.id).first()
        if x == None:
            # give default image
            return url_for('static', filename='/images/Noimage.png')
        else:
            if x.imageone == '0':
                return url_for('static', filename='/images/Noimage.png')
            else:
            # get primary image
                return url_for('userdata.media_file', nodeid=x.stringnodeid, filename=('item/' + x.string + x.imageone))
    elif type == 2:
        pass

    elif type == 3:
        pass
    else:
        pass
