from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.profile import profile
from app import db
# models
from app.classes.auth import User
from app.classes.achievements import \
    UserAchievements, \
    whichAch, \
    UserAchievements_recent

from app.classes.item import \
    marketitem

from app.classes.profile import \
    Userreviews, \
    exptable, \
    StatisticsUser, \
    StatisticsVendor

from app.classes.userdata import \
    Feedback


from app.classes.wallet_bch import \
    BchWallet

from datetime import \
    datetime
from app.common.functions import \
    floating_decimals

from flask_paginate import Pagination, get_page_args
from sqlalchemy.sql import func
from app.profile.profilebar import profilebar
from app.common.decorators import website_offline


@profile.route('/<string:username>', methods=['GET', 'POST'])
@website_offline
def frontpage(username):
    now = datetime.utcnow()

    if username != 'Guest':
        user = db.session.query(User).filter_by(username=username).first()
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
                .query(UserAchievements_recent) \
                .filter_by(user_id=user.id) \
                .order_by(UserAchievements_recent.achievement_date.desc()) \
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


@profile.route('/c/<string:username>', methods=['GET'])
@website_offline
def user(username):
    page, per_page, offset = get_page_args()
    # PEr Page tells how many search results pages
    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 20
    now = datetime.utcnow()

    user = db.session.query(User).filter_by(username=username).first()
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

        # stats
        stats = db.session\
            .query(StatisticsUser)\
            .filter_by(username=user.username)\
            .first()

        started = stats.startedbuying.strftime("%m/%d/%y")

        # User reviews
        getratings = db.session\
            .query(Userreviews)\
            .filter(Userreviews.customer == user.username)\
            .order_by(Userreviews.dateofreview.desc())

        usercount = getratings.count()
        userreview = getratings.limit(per_page).offset(offset)

        paginationuserreview = Pagination(page=page,
                                          total=getratings.count(),
                                          search=False,
                                          record_name='items',
                                          offset=offset,
                                          per_page=per_page,
                                          css_framework='bootstrap4',
                                          inner_window=inner_window,
                                          outer_window=outer_window)

        return render_template('profile/customer.html',
                               user=user, now=now,
                               userreview=userreview,
                               usercount=usercount,
                               paginationuserreview=paginationuserreview,
                               stats=stats,
                               started=started,
                               user1=user1,
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


@profile.route('/v/<string:username>', methods=['GET', 'POST'])
@website_offline
def vendorprofile(username):
    now = datetime.utcnow()
    # vendor
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        if user.vendor_account == 1:
            search = False
            q = request.args.get('q')
            if q:
                search = True
            page, per_page, offset = get_page_args()

            # PEr Page tells how many search results pages
            inner_window = 5  # search bar at bottom used for .. lots of pages
            outer_window = 5  # search bar at bottom used for .. lots of pages
            per_page = 20

            # vendorwallet = db.session.query(BtcWallet).filter_by(user_id=vendor.id).first()
            vendorstats = db.session\
                .query(StatisticsVendor)\
                .filter_by(vendorid=user.id)\
                .first()

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

            # GEt started time

            started = vendorstats.startedselling.strftime("%m/%d/%y")

            ratingsall = db.session\
                .query(Feedback)\
                .filter_by(vendorid=user.id)\
                .order_by(Feedback.timestamp.desc())
            ratingscount = ratingsall.count()
            ratings = ratingsall.limit(per_page).offset(offset)

            paginationvendorreview = Pagination(page=page,
                                                total=ratingsall.count(),
                                                search=search,
                                                record_name='items',
                                                offset=offset,
                                                per_page=per_page,
                                                css_framework='bootstrap4',
                                                inner_window=inner_window,
                                                outer_window=outer_window)

            getavgitem = db.session.query(
                func.avg(Feedback.item_rating).label("avgitem"))
            getavgitem = getavgitem.filter(Feedback.vendorid == user.id)
            gitem = getavgitem.all()
            itemscore = str((gitem[0][0]))[:4]
            if itemscore == 'None':
                itemscore = 0
            getavgvendor = db.session.query(
                func.avg(Feedback.vendorrating).label("avgvendor"))
            getavgvendor = getavgvendor.filter(Feedback.vendorid == user.id)
            gvendor = getavgvendor.all()
            vendorscore = str((gvendor[0][0]))[:4]
            if vendorscore == 'None':
                vendorscore = 0

            return render_template('/profile/vendor.html',
                                   started=started,
                                   user=user,
                                   ratings=ratings,
                                   itemscore=itemscore,
                                   vendorscore=vendorscore,
                                   vendorstats=vendorstats,
                                   ratingscount=ratingscount,
                                   now=now,
                                   paginationvendorreview=paginationvendorreview,
                                   user1=user1,
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
            flash("This user isnt a vendor", category="danger")
            return redirect(url_for('profile.frontpage', username=user.username))
    else:
        flash("This user doesnt exist", category="danger")
        return redirect(url_for('index'))


@profile.route('/store/<username>', methods=['GET', 'POST'])
@website_offline
def vendorStore(username):
    now = datetime.utcnow()
    # vendor
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        if user.vendor_account == 1:
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

            # get users top market items
            getitems = db.session\
                .query(marketitem) \
                .filter(marketitem.vendor_id == user.id, marketitem.online == 1) \
                .order_by(marketitem.total_sold.desc()) \
                .limit(3)

            # get users newest market items
            getnewitems = db.session\
                .query(marketitem) \
                .filter(marketitem.vendor_id == user.id, marketitem.online == 1) \
                .order_by(marketitem.created.desc()) \
                .limit(3)
            getitemscount = db.session\
                .query(marketitem)\
                .filter(marketitem.vendor_id == user.id)\
                .count()

            # # Get user Store
            # # market item queries
            # # join subcategories for the marketitem
            # allcategory = db.session.query(func.count(marketitem.category_id_0).label("catcount"),
            #                                Cats.catname0,
            #                                Cats.id,
            #                                Cats.id.label("itemnumber"))
            # allcategory = allcategory.join(Cats.catid0)
            # allcategory = allcategory.filter(marketitem.subcategory == Cats.id)
            # allcategory = allcategory.filter(marketitem.vendor_id == vendor.id)
            # allcategory = allcategory.filter(marketitem.online == 1)
            # allcategory = allcategory.group_by(Cats.catname0, Cats.id)
            # allcat = allcategory.all()

            return render_template('/profile/vendorstore/storeHomepage.html',
                                   now=now,
                                   getitems=getitems,
                                   getnewitems=getnewitems,
                                   getitemscount=getitemscount,
                                   user=user,
                                   user1=user1,
                                   user1width=user1width,
                                   user1level=user1level,
                                   user1pictureid=user1pictureid,
                                   user1wallet=user1wallet,
                                   user1stats=user1stats,
                                   user1ach=user1ach,
                                   user1vendorstats=user1vendorstats,
                                   )
        else:
            flash("This user isnt a vendor", category="danger")
            return redirect(url_for('profile.frontpage', username=user.username))
    else:
        flash("This user doesnt exist", category="danger")
        return redirect(url_for('index'))
