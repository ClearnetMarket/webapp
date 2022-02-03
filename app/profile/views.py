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
    marketItem

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
                func.avg(Feedback.itemrating).label("avgitem"))
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


@profile.route('/achievements-all/<username>', methods=['GET', 'POST'])
@website_offline
def achs(username):
    if username != 'Guest':

        user = db.session\
            .query(User)\
            .filter_by(username=username)\
            .first()
        title = user.username + "'s Achievements"
        usergetlevel = db.session\
            .query(UserAchievements)\
            .filter_by(username=user.username)\
            .first()
        userpictureid = str(usergetlevel.level)
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=user.id)\
            .first()
        userstats = db.session\
            .query(StatisticsUser)\
            .filter_by(username=user.username)\
            .first()
        level = db.session\
            .query(UserAchievements)\
            .filter_by(username=user.username)\
            .first()
        nextlevel = level.level + 1
        userach = db.session\
            .query(whichAch)\
            .filter_by(user_id=user.id)\
            .first()
        user_recent_ach = db.session\
            .query(UserAchievements_recent)\
            .filter_by(user_id=user.id)\
            .order_by(UserAchievements_recent.achievement_date.desc())\
            .limit(10)

        if 1 <= level.level <= 3:
            user1widthh = (level.experiencepoints / 300) * 100
            width = floating_decimals(user1widthh, 0)
        elif 4 <= level.level <= 7:
            user1widthh = (level.experiencepoints / 500) * 100
            width = floating_decimals(user1widthh, 0)
        elif 8 <= level.level <= 10:
            user1widthh = (level.experiencepoints / 1000) * 100
            width = floating_decimals(user1widthh, 0)
        elif 11 <= level.level <= 14:
            user1widthh = (level.experiencepoints / 1500) * 100
            width = floating_decimals(user1widthh, 0)
        elif 16 <= level.level <= 20:
            user1widthh = (level.experiencepoints / 2000) * 100
            width = floating_decimals(user1widthh, 0)
        elif 21 <= level.level <= 25:
            user1widthh = (level.experiencepoints / 2250) * 100
            width = floating_decimals(user1widthh, 0)
        elif 26 <= level.level <= 30:
            user1widthh = (level.experiencepoints / 2500) * 100
            width = floating_decimals(user1widthh, 0)
        elif 26 <= level.level <= 30:
            user1widthh = (level.experiencepoints / 3000) * 100
            width = floating_decimals(user1widthh, 0)
        elif 26 <= level.level <= 30:
            user1widthh = (level.experiencepoints / 4000) * 100
            width = floating_decimals(user1widthh, 0)
        elif 30 <= level.level <= 50:
            user1widthh = (level.experiencepoints / 5000) * 100
            width = floating_decimals(user1widthh, 0)
        elif 51 <= level.level <= 100:
            user1widthh = (level.experiencepoints / 10000) * 100
            width = floating_decimals(user1widthh, 0)
        else:
            user1widthh = (level.experiencepoints / 1000) * 100
            width = floating_decimals(user1widthh, 0)

        # getuser exp table
        userexp = db.session\
            .query(exptable)\
            .filter(user.id == exptable.user_id)\
            .order_by(exptable.timestamp.desc())
        exp = userexp.limit(10)
        expcount = userexp.count()
        return render_template('/profile/userachievements/achievementsall.html',
                               title=title,
                               user=user,
                               width=width,
                               level=level,
                               usergetlevel=usergetlevel,
                               userpictureid=userpictureid,
                               userwallet=userwallet,
                               userstats=userstats,
                               exp=exp, expcount=expcount,
                               userach=userach,
                               nextlevel=nextlevel,
                               user_recent_ach=user_recent_ach
                               )
    else:
        flash("User does not have an account", category="danger")
        return redirect(url_for('index', username=current_user.username))


@profile.route('/achievements-coin/<username>', methods=['GET', 'POST'])
@website_offline
def achievements_coin(username):
    user = db.session.query(User).filter_by(username=username).first()
    title = user.username + "'s Achievements"

    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        my_none = '1'
        nodate = 'date'
        noid = 'id'
        nouser_id = 'user_id'
        nolevel = 'level'
        noexp = 'experiencepoints'
        nousername = 'username'
        solutions = []
        for key, value in d.items():

            if my_none in value:
                if nousername not in key:
                    if nodate not in key:
                        if nolevel not in key:
                            if noid not in key:
                                if nouser_id not in key:
                                    if noexp not in key:
                                        solutions.append(key)

        x = solutions
        size = len(x)
        return x, size

    x, size = row2dict(row=db.session.query(
        UserAchievements).filter_by(user_id=user.id).first())

    return render_template('/profile/userachievements/achievementscoin.html',
                           x=x,
                           size=size,
                           title=title,
                           user=user
                           )


@profile.route('/achievements-common/<username>', methods=['GET', 'POST'])
@website_offline
def achievements_common(username):
    user = db.session.query(User).filter_by(username=username).first()
    title = user.username + "'s Achievements"

    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        my_none = '1'
        nodate = 'date'
        noid = 'id'
        nouser_id = 'user_id'
        nolevel = 'level'
        noexp = 'experiencepoints'
        nousername = 'username'
        solutions = []
        for key, value in d.items():

            if my_none in value:
                if nousername not in key:
                    if nodate not in key:
                        if nolevel not in key:
                            if noid not in key:
                                if nouser_id not in key:
                                    if noexp not in key:
                                        solutions.append(key)
        x = solutions
        size = len(x)
        return x, size

    x, size = row2dict(row=db.session.query(
        UserAchievements).filter_by(user_id=user.id).first())
    return render_template('/profile/userachievements/achievementscommon.html',
                           x=x,
                           size=size,
                           title=title,
                           user=user
                           )


@profile.route('/achievements-experience/<username>', methods=['GET', 'POST'])
@website_offline
def achievements_experience(username):
    user = db.session.query(User).filter_by(username=username).first()
    title = user.username + "'s Achievements"

    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        my_none = '1'
        nodate = 'date'
        noid = 'id'
        nouser_id = 'user_id'
        nolevel = 'level'
        noexp = 'experiencepoints'
        nousername = 'username'
        solutions = []
        for key, value in d.items():
            if my_none in value:
                if nousername not in key:
                    if nodate not in key:
                        if nolevel not in key:
                            if noid not in key:
                                if nouser_id not in key:
                                    if noexp not in key:
                                        solutions.append(key)
        x = solutions
        size = len(x)
        return x, size
    x, size = row2dict(row=db.session.query(
        UserAchievements).filter_by(user_id=user.id).first())
    return render_template('/profile/userachievements/achievementsExperience.html',
                           x=x,
                           size=size,
                           title=title,
                           user=user
                           )


@profile.route('/auth-achievements-unique/<username>', methods=['GET', 'POST'])
@website_offline
def achievements_unique(username):
    user = db.session.query(User).filter_by(username=username).first()
    title = user.username + "'s Achievements"

    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        my_none = '1'
        nodate = 'date'
        noid = 'id'
        nouser_id = 'user_id'
        nolevel = 'level'
        noexp = 'experiencepoints'
        nousername = 'username'
        solutions = []
        for key, value in d.items():
            if my_none in value:
                if nousername not in key:
                    if nodate not in key:
                        if nolevel not in key:
                            if noid not in key:
                                if nouser_id not in key:
                                    if noexp not in key:
                                        solutions.append(key)
        x = solutions
        size = len(x)
        return x, size

    x, size = row2dict(row=db.session.query(
        UserAchievements).filter_by(user_id=user.id).first())
    return render_template('/profile/userachievements/achievementsunique.html',
                           x=x,
                           size=size,
                           title=title,
                           user=user
                           )


@profile.route('/achievements-customer/<username>', methods=['GET', 'POST'])
@website_offline
def achievements_customer(username):
    user = db.session.query(User).filter_by(username=username).first()
    title = user.username + "'s Achievements"

    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        my_none = '1'
        nodate = 'date'
        noid = 'id'
        nouser_id = 'user_id'
        nolevel = 'level'
        noexp = 'experiencepoints'
        nousername = 'username'
        solutions = []
        for key, value in d.items():
            if my_none in value:
                if nousername not in key:
                    if nodate not in key:
                        if nolevel not in key:
                            if noid not in key:
                                if nouser_id not in key:
                                    if noexp not in key:
                                        solutions.append(key)
        x = solutions
        size = len(x)
        return x, size

    x, size = row2dict(row=db.session.query(
        UserAchievements).filter_by(user_id=user.id).first())
    return render_template('/profile/userachievements/achievementscustomer.html',
                           x=x,
                           size=size,
                           title=title,
                           user=user
                           )


@profile.route('/achievements-vendor/<username>', methods=['GET', 'POST'])
@website_offline
def achievements_vendor(username):
    user = db.session.query(User).filter_by(username=username).first()
    title = user.username + "'s Achievements"

    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        my_none = '1'
        nodate = 'date'
        noid = 'id'
        nouser_id = 'user_id'
        nolevel = 'level'
        noexp = 'experiencepoints'
        nousername = 'username'
        solutions = []
        for key, value in d.items():
            if my_none in value:
                if nousername not in key:
                    if nodate not in key:
                        if nolevel not in key:
                            if noid not in key:
                                if nouser_id not in key:
                                    if noexp not in key:
                                        solutions.append(key)
        x = solutions
        size = len(x)
        return x, size

    x, size = row2dict(row=db.session.query(
        UserAchievements).filter_by(user_id=user.id).first())
    return render_template('/profile/userachievements/achievementsvendor.html',
                           x=x,
                           size=size,
                           title=title,
                           user=user
                           )


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
                .query(marketItem) \
                .filter(marketItem.vendor_id == user.id, marketItem.online == 1) \
                .order_by(marketItem.totalsold.desc()) \
                .limit(3)

            # get users newest market items
            getnewitems = db.session\
                .query(marketItem) \
                .filter(marketItem.vendor_id == user.id, marketItem.online == 1) \
                .order_by(marketItem.created.desc()) \
                .limit(3)
            getitemscount = db.session\
                .query(marketItem)\
                .filter(marketItem.vendor_id == user.id)\
                .count()

            # # Get user Store
            # # market item queries
            # # join subcategories for the marketitem
            # allcategory = db.session.query(func.count(marketItem.categoryid0).label("catcount"),
            #                                Cats.catname0,
            #                                Cats.id,
            #                                Cats.id.label("itemnumber"))
            # allcategory = allcategory.join(Cats.catid0)
            # allcategory = allcategory.filter(marketItem.subcategory == Cats.id)
            # allcategory = allcategory.filter(marketItem.vendor_id == vendor.id)
            # allcategory = allcategory.filter(marketItem.online == 1)
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
