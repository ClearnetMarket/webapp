from flask import \
    render_template, \
    redirect, \
    url_for, \
    g, \
    session, \
    flash, \
    Response, \
    send_from_directory

from flask_login import current_user
from app.main import main
from app import db, app, UPLOADED_FILES_DEST
from flask_paginate import Pagination, get_page_args

from flask import request
# models
from app.classes.auth import User
from app.classes.achievements import \
    Achievements, \
    UserAchievements_recent

from app.classes.affiliate import \
    AffiliateOverview, \
    AffiliateStats
from app.classes.item import \
    marketItem
from app.classes.category import Categories
from app.classes.message import \
    Notifications

from app.classes.vendor import \
    Orders

from app.classes.models import \
    btc_cash_Prices

# End Models
from app.profile.profilebar import profilebar

from app.auth.forms import searchForm
from app.search.searchfunction import headerfunctions_vendor, headerfunctions
from datetime import timedelta, datetime
from app.common.functions import btc_cash_convertlocaltobtc
import os
from decimal import Decimal
from sqlalchemy.sql.expression import func
from app.common.decorators import website_offline, \
    ping_user, \
    login_required


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    def Disallow(string): return 'Disallow: {0}'.format(string)
    return Response("User-agent: *\n{0}\n".format("\n".join([
        Disallow('/bin/*'),
        Disallow('/wallet_btc'),
        Disallow('/admin'),
    ])))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@website_offline
def index():

    now = datetime.utcnow()
    # forms
    formsearch = searchForm()

    user, \
        order, \
        tot, \
        issues, \
        getnotifications, \
        allmsgcount, \
        userbalance, \
        unconfirmed, \
        customerdisputes = headerfunctions()

    btc_cash_price = db.session\
        .query(btc_cash_Prices)\
        .all()

    get_cats = db.session\
        .query(Categories)\
        .filter(Categories.id != 1000, Categories.id != 0)\
        .order_by(Categories.name.asc())\
        .all()

    if current_user.is_authenticated:

        user1, \
            user1pictureid, \
            user1stats, \
            user1wallet, \
            user1level, \
            user1width, \
            user1ach, \
            user1vendorstats, \
            user2getlevel, \
            user2pictureid, \
            user2stats, \
            user2wallet, \
            user2level, \
            user2width, \
            user2ach, \
            user2vendorstats, \
            user2 = profilebar(user_id1=user.id, user_id2=0)

        user_recent_ach = db.session\
            .query(UserAchievements_recent) \
            .filter_by(user_id=user.id) \
            .order_by(UserAchievements_recent.achievement_date.desc()) \
            .limit(10)

        if current_user.affiliate_account != 0:
            try:
                # users promo overview
                userpromooverview = db.session\
                    .query(AffiliateOverview)\
                    .filter_by(user_id=current_user.id)\
                    .first()
                # users promo stats
                userpromostats = db.session\
                    .query(AffiliateStats)\
                    .filter_by(user_id=current_user.id)\
                    .first()
            except Exception:
                userpromooverview = None
                userpromostats = None
        else:
            userpromooverview = None
            userpromostats = None

        try:
            # Get Vendor needs return address
            ordersifreturnvendor = db.session\
                .query(Orders)\
                .filter(Orders.vendor_id == current_user.id)\
                .filter(Orders.request_return == 1)
            returnneededvendoraddress = ordersifreturnvendor.count()
        except Exception:
            returnneededvendoraddress = None

        try:
            # Get Vendor needs mark as returned
            ordersifreturnvendor = db.session\
                .query(Orders)\
                .filter(Orders.vendor_id == current_user.id)\
                .filter(Orders.request_return == 3)\
                .count()
        except Exception:
            ordersifreturnvendor = None

        # flash new achievements
        try:
            user_recent_achievements = db.session\
                .query(UserAchievements_recent)\
                .filter_by(user_id=current_user.id, viewed=0)\
                .limit(10)
            if user_recent_achievements:
                for f in user_recent_achievements:
                    x = int(f.ach_id)
                    flash(x, 1)
                    f.viewed = 1
                    db.session.add(f)
                db.session.commit()
        except Exception:
            pass

        # Newest Items
        todayfeaturedfull = db.session\
            .query(marketItem)\
            .filter(marketItem.online == 1)\
            .filter(marketItem.imageone != '')\
            .order_by(marketItem.created.desc())
        todayfeatured = todayfeaturedfull.limit(5)
        tfcount = todayfeaturedfull.count()
        # best sellers
        bestsellersfull = db.session\
            .query(marketItem)\
            .filter(marketItem.online == 1)\
            .filter(marketItem.imageone != '')\
            .order_by(marketItem.totalsold.desc())
        bestsellers = bestsellersfull.limit(5)
        bestsellerscount = bestsellersfull.count()
        # Electronics
        electronicsfull = db.session\
            .query(marketItem)\
            .filter(marketItem.online == 1)\
            .filter(marketItem.imageone != '')\
            .filter(marketItem.categoryid0 == 9)\
            .order_by(func.random())
        Electronics = electronicsfull.limit(5)
        Electronicscount = electronicsfull.count()
        # PROMOTED
        additemfull = db.session\
            .query(marketItem)\
            .filter(marketItem.online == 1)\
            .filter(marketItem.imageone != "")\
            .filter(marketItem.aditem == 1)\
            .filter(marketItem.aditem_level == 2)\
            .order_by(func.random())
        promoteditems = additemfull.limit(45)
        promoteditemscount = additemfull.count()

    else:
        # Newest Items
        todayfeaturedfull = db.session\
            .query(marketItem)\
            .filter(marketItem.online == 1)\
            .filter(marketItem.imageone != '')\
            .order_by(marketItem.created.desc())
        todayfeatured = todayfeaturedfull.limit(5)
        tfcount = todayfeaturedfull.count()
        # best sellers
        bestsellersfull = db.session\
            .query(marketItem)\
            .filter(marketItem.online == 1)\
            .filter(marketItem.imageone != '')\
            .order_by(marketItem.totalsold.desc())
        bestsellers = bestsellersfull.limit(5)
        bestsellerscount = bestsellersfull.count()
        # Electronics
        electronicsfull = db.session\
            .query(marketItem)\
            .filter(marketItem.online == 1)\
            .filter(marketItem.categoryid0 == 9)\
            .order_by(func.random())
        Electronics = electronicsfull.limit(5)
        Electronicscount = electronicsfull.count()
        # PROMOTED
        additemfull = db.session\
            .query(marketItem)\
            .filter(marketItem.online == 1)\
            .filter(marketItem.aditem == 1)\
            .filter(marketItem.aditem_level == 2)\
            .order_by(func.random())
        promoteditems = additemfull.limit(5)
        promoteditemscount = additemfull.count()

        # variables---poor coding?
        userpromooverview = None
        userpromostats = None
        user1 = None
        user1width = None
        user1level = None
        user1pictureid = None
        user1wallet = None
        user1stats = None
        user1ach = None
        user1vendorstats = None
        user_recent_ach = 0
        returnneededvendoraddress = None
        ordersifreturnvendor = None

    if request.method == 'POST':
        print(formsearch.data)

        if formsearch.data and formsearch.validate_on_submit():

            categoryfull = formsearch.category.data
            cat = categoryfull.id
            print(cat)
            if formsearch.searchString.data == '' and cat == 0:
                return redirect(url_for('index'))
            if formsearch.searchString.data == '':
                formsearch.searchString.data = cat
            return redirect(url_for('search.searchMaster',
                                    searchterm=formsearch.searchString.data,
                                    function=cat,
                                    ))
    return render_template('index.html',
                           UPLOADED_FILES_DEST=UPLOADED_FILES_DEST,
                           # forms
                           form=formsearch,
                           # header stuff
                           user=user,
                           now=now,
                           order=order,
                           tot=tot,
                           issues=issues,
                           getnotifications=getnotifications,
                           allmsgcount=allmsgcount,
                           userbalance=userbalance,
                           unconfirmed=unconfirmed,
                           # btc prices
                           btc_cash_price=btc_cash_price,
                           # page queries
                           get_cats=get_cats,
                           todayfeatured=todayfeatured,
                           bestsellers=bestsellers,
                           Electronics=Electronics,
                           Electronicscount=Electronicscount,
                           # return flashes sidebar
                           returnneededvendoraddress=returnneededvendoraddress,
                           ordersifreturnvendor=ordersifreturnvendor,
                           tfcount=tfcount,
                           bestsellerscount=bestsellerscount,
                           customerdisputes=customerdisputes,
                           # profile bar
                           user1=user1,
                           user1width=user1width,
                           user1level=user1level,
                           user1pictureid=user1pictureid,
                           user1wallet=user1wallet,
                           user1stats=user1stats,
                           user1ach=user1ach,
                           user1vendorstats=user1vendorstats,
                           user_recent_ach=user_recent_ach,
                           # affiliate bar
                           userpromooverview=userpromooverview,
                           userpromostats=userpromostats,
                           # promotions
                           promoteditems=promoteditems,
                           promoteditemscount=promoteditemscount
                           )


@main.route('/about', methods=['GET', 'POST'])
@website_offline
def about():
    return render_template('/general/about.html')


@main.route('/notifications/', methods=['GET', 'POST'])
@website_offline
@login_required
def notifications():
    now = datetime.utcnow()
    from app.message.forms import topbuttonForm
    user, \
        order, \
        issues, \
        getnotifications, \
        customerdisputes \
        = headerfunctions_vendor()
    delormarkasread = topbuttonForm()
    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()
    # Pagination
    search = False
    page, per_page, offset = get_page_args()
    # Per Page tells how many search results pages
    inner_window = 1  # search bar at bottom used for .. lots of pages
    outer_window = 1  # search bar at bottom used for .. lots of pages

    getnotes = db.session\
        .query(Notifications)\
        .filter(Notifications.user_id == user.id)\
        .order_by(Notifications.timestamp.desc())

    notifications = getnotes.limit(per_page).offset(offset)
    pagination = Pagination(page=page,
                            total=getnotes.count(),
                            search=search,
                            record_name='items',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap4',
                            inner_window=inner_window,
                            outer_window=outer_window)

    if request.method == "POST":
        for v in request.form.getlist('checkit'):
            if delormarkasread.delete.data:
                specific_note = db.session.query(
                    Notifications).filter_by(id=v).first()
                if specific_note:
                    if specific_note.user_id == current_user.id:
                        db.session.delete(specific_note)
                    else:
                        flash("Error", category="danger")

            elif delormarkasread.markasread.data:
                specific_note = db.session.query(
                    Notifications).filter_by(id=v).first()
                if specific_note.user_id == current_user.id:
                    if specific_note.read == 1:
                        specific_note.read = 0
                        db.session.add(specific_note)

                else:
                    flash("Error", category="danger")
        db.session.commit()
        return redirect(url_for('main.notifications', username=current_user.username))
    return render_template('notifications.html',
                           notifications=notifications,
                           pagination=pagination,
                           user=user,
                           now=now,
                           delormarkasread=delormarkasread,
                           order=order,
                           issues=issues,
                           getnotifications=getnotifications,
                           customerdisputes=customerdisputes
                           )


@main.route('/termsofservice', methods=['GET', 'POST'])
@website_offline
def termsofservice():
    return render_template('/tos.html')


@main.route('/contact', methods=['GET', 'POST'])
@website_offline
def contact():
    return render_template('/contact.html')


@main.route('/privacystatement', methods=['GET', 'POST'])
@website_offline
def privacy():
    return render_template('/privacy.html')


@main.route('/bugbounty', methods=['GET', 'POST'])
def bugbounty():
    return render_template('/general/bugbounty.html')


@main.route('/clearnetdown')
def offline():
    ##status = 2
    return render_template('/errors/offline.html')


@main.route('/clearnetbusy')
def busy():
    ##status = 3
    return render_template('/errors/busy.html')


@main.route('/clearnetmaitenance')
def scheduledmaintenance():
    ##status = 1
    return render_template('/errors/schmait.html')


@main.route('/levels')
@website_offline
def levels():
    hundred = btc_cash_convertlocaltobtc(amount=100, currency=0)
    twofity = btc_cash_convertlocaltobtc(amount=250, currency=0)
    fivehundred = btc_cash_convertlocaltobtc(amount=500, currency=0)
    thousand = btc_cash_convertlocaltobtc(amount=1000, currency=0)
    twentyfivehundred = btc_cash_convertlocaltobtc(amount=2500, currency=0)

    hundred = Decimal(hundred)
    twofity = Decimal(twofity)
    fivehundred = Decimal(fivehundred)
    thousand = Decimal(thousand)
    twentyfivehundred = Decimal(twentyfivehundred)

    return render_template('/general/trustandlevels.html',
                           hundred=hundred,
                           twofity=twofity,
                           fivehundred=fivehundred,
                           thousand=thousand,
                           twentyfivehundred=twentyfivehundred
                           )


@main.route('/banned')
@website_offline
def whybanned():
    return render_template('/general/bannedandwhy.html')


@main.route('/careers')
@website_offline
def careers():
    return render_template('/general/careers.html')


@app.route('/<username>', methods=['GET'])
@website_offline
def frontpage(username):
    from app.profile.profilebar import profilebar

    now = datetime.utcnow()

    if username != 'Guest':
        user = db.session\
            .query(User)\
            .filter_by(username=username)\
            .first()
        if user:
            user1, \
                user1pictureid, \
                user1stats, \
                user1wallet, \
                user1level, \
                user1width, \
                user1ach, \
                user1vendorstats, \
                user2getlevel, \
                user2pictureid, \
                user2stats, \
                user2wallet, \
                user2level, \
                user2width, \
                user2ach, \
                user2vendorstats, \
                user2 = profilebar(user_id1=user.id, user_id2=0)

            user_recent_ach = db.session\
                .query(UserAchievements_recent)\
                .filter_by(user_id=user.id)\
                .order_by(UserAchievements_recent.achievement_date.desc())\
                .limit(10)

            return render_template('profile/overview.html',
                                   user1=user1,
                                   user=user,
                                   now=now,
                                   user1width=user1width,
                                   user1level=user1level,
                                   user1pictureid=user1pictureid,
                                   user1wallet=user1wallet,
                                   user1stats=user1stats,
                                   user1ach=user1ach,
                                   user1vendorstats=user1vendorstats,
                                   user_recent_ach=user_recent_ach

                                   )

        else:
            flash("User does not have an account", category="danger")
            return redirect(url_for('index', username=current_user.username))
    else:
        flash("User does not have an account", category="danger")
        return redirect(url_for('index', username=current_user.username))


@main.route('/advertise')
@website_offline
def advertise():
    return render_template('/general/advertise.html')
