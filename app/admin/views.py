from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.admin import admin
from app import db

from app.admin.forms import \
    addachievement, \
    settoAdmin, \
    addupdateform, \
    Chatform, \
    Disputeform, \
    searchadminForm, \
    Userform, \
    adminsendMoney, \
    changeitemForm, \
    changeUserForm

from app.wallet_bch.wallet_btccash_work import\
    btc_cash_send_coin_to_user_as_admin, \
    btc_cash_takeCointoUser_asAdmin
# models
from app.classes.auth import \
    User

from app.classes.achievements import \
    Achievements, \
    UserAchievements, \
    whichAch

from app.classes.admin import \
    clearnetprofit_btc, \
    flagged

from app.classes.item import \
    marketItem

from app.classes.message import \
    Chat, \
    PostUser, \
    Comment

from app.classes.profile import \
    Userreviews, \
    StatisticsUser, \
    StatisticsVendor

from app.classes.service import \
    shippingSecret, \
    websitefeedback, \
    updateLog, Tracking, Issue

from app.classes.userdata import \
    Feedback

from app.classes.vendor import \
    Orders

# end models
from app.notification import notification

from app.wallet_bch.wallet_btccash_work import \
    btc_cash_sendCointoUser

from app.common.query import achievementcategory
from app.classes.wallet_bch import *

from decimal import Decimal
from datetime import datetime, timedelta

from flask_paginate import Pagination, get_page_args

from app.common.decorators import \
    ADMINaccount_required, \
    ADMINaccountlevel10_required, \
    login_required, \
    ADMINaccountlevel3_required, \
    ping_user, \
    website_offline


@admin.route('/', methods=['GET', 'POST'])
@website_offline
@ping_user
@login_required
@ADMINaccount_required
@ADMINaccountlevel3_required
def adminHome():
    now = datetime.utcnow()
    form = searchadminForm(request.form)

    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass

    # User
    user = db.session.query(User).filter_by(
        username=current_user.username).first()
    usergetlevel = db.session.query(UserAchievements).filter_by(
        username=user.username).first()
    userpictureid = str(usergetlevel.level)
    userstats = db.session.query(StatisticsUser).filter_by(
        username=user.username).first()

    level = db.session.query(UserAchievements).filter_by(
        username=user.username).first()
    width = int(level.experiencepoints / 10)
    userach = db.session.query(whichAch).filter_by(user_id=user.id).first()

    # get orders mods are currently working on
    modsorders = db.session.query(Orders)
    modsorders = modsorders.filter(Orders.disputed_order == 1)
    modsorders = modsorders.filter(Orders.modid == user.id)
    modsorders = modsorders.order_by(Orders.disputedtimer.desc())
    modorders = modsorders.all()
    modorderscount = modsorders.count()

    # get disputes items
    disputesitem = db.session.query(Orders)
    disputesitem = disputesitem.filter(Orders.disputed_order == 1)
    disputesitem = disputesitem.filter(Orders.type == 1)
    disputesitem = disputesitem.filter(Orders.modid == 0)
    disputesitem = disputesitem.order_by(Orders.disputedtimer.desc())
    itemdisputes = disputesitem.limit(20)
    countitemdisputes = disputesitem.count()

    # get customer help/messages
    allmsgs_mod = db.session.query(Issue)
    allmsgs_mod = allmsgs_mod.filter(Issue.status == 0)
    msgs_mod = allmsgs_mod.limit(10)
    msgs_mod_count = allmsgs_mod.count()

    # get flagged items
    items = db.session.query(flagged)
    items = items.order_by(flagged.howmany.desc())
    item = items.all()
    countitem = items.count()

    # get msgs mods are currently working on
    my_mod = db.session.query(PostUser)
    my_mod = my_mod.filter(PostUser.official == 1)
    my_mod = my_mod.filter(PostUser.user_id == 0)
    my_mod = my_mod.filter(PostUser.modid == current_user.id)
    currentmod_mod = my_mod.limit(10)
    currentmod_count = my_mod.count()

    allfeedback = db.session.query(websitefeedback)
    allfeedback = allfeedback.order_by(websitefeedback.timestamp.desc())
    feedback = allfeedback.all()

    if request.method == 'POST':

        if form.finduser.data:
            return redirect(url_for('admin.admin_viewuser', username=form.searchbar.data))
        if form.findorder.data:
            return redirect(url_for('admin.admin_vieworder', id=form.searchbar.data))
        if form.finditem.data:
            return redirect(url_for('admin.admin_viewitem', id=form.searchbar.data))
        if form.change_usersearch.data:
            return redirect(url_for('admin.changeuser', username=form.changeuser_searchbar.data))
        else:
            pass

    return render_template('admin/admin_home.html',
                           user=user,
                           now=now,
                           item=item,
                           countitem=countitem,
                           userpictureid=userpictureid,
                           usergetlevel=usergetlevel,

                           modorders=modorders,
                           modorderscount=modorderscount,
                           feedback=feedback,
                           level=level,
                           width=width,
                           userstats=userstats,
                           itemdisputes=itemdisputes,
                           countitemdisputes=countitemdisputes,
                           msgs_mod_count=msgs_mod_count,
                           msgs_mod=msgs_mod,
                           form=form,
                           userach=userach,

                           currentmod_mod=currentmod_mod,
                           currentmod_count=currentmod_count,
                           )


@admin.route('/changeitem/', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel10_required
def changeitem():
    form = changeitemForm(request.form)
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass

    if request.method == 'POST':
        if current_user.admin == 1:
            if form.finditem.data:
                getitem = db.session.query(marketItem).filter_by(
                    id=form.searchbar.data).first()
                if getitem:
                    try:
                        addfeed = Feedback(
                            customername='eddwinn',
                            sale_id=0,
                            vendorname=getitem.vendor_name,
                            vendorid=getitem.vendor_id,
                            comment=form.comment.data,
                            itemrating=form.itemrating.data,
                            item_id=form.searchbar.data,
                            type=1,
                            vendorrating=form.vendorrating.data,
                            timestamp=datetime.utcnow(),
                            addedtodb=1,
                            author_id=0,
                        )

                        db.session.add(addfeed)
                        db.session.commit()

                        # increase vendor stats
                        getvendor = db.session.query(StatisticsVendor).filter_by(
                            vendorid=getitem.vendor_id).first()
                        x = getvendor.totalsales
                        y = x + 1

                        a = getvendor.diffpartners
                        b = a + 1

                        d = getvendor.totalreviews
                        e = d + 1

                        getvendor.totalreviews = e
                        getvendor.totalsales = y
                        getvendor.diffpartners = b

                        db.session.add(getvendor)
                        db.session.commit()
                        flash("Item Updated", category="success")
                        return redirect(url_for('admin.changeitem'))
                    except Exception as e:
                        db.session.rollback()
                        flash("error: " + str(e), category="danger")
                        return redirect(url_for('admin.changeitem'))
                else:
                    flash("No item with that id", category="danger")
                    return redirect(url_for('admin.changeitem'))
            else:
                pass

    return render_template('admin/god/changeitem.html',
                           form=form
                           )


@admin.route('/changeuser/<username>', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel10_required
def changeuser(username):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass

    getstatscustomer = db.session.query(
        StatisticsUser).filter_by(username=username).first()
    getstatsvendor = db.session.query(
        StatisticsVendor).filter_by(username=username).first()
    form = changeUserForm(
        customer_totalitemsbought=getstatscustomer.totalitemsbought,
        customer_totalreviews=getstatscustomer.totalreviews,
        customer_totaltrades=getstatscustomer.totaltrades,
        customer_totalbtcrecieved=getstatscustomer.totalbtcrecieved,
        customer_totalbtcspent=getstatscustomer.totalbtcspent,
        difftradingpartners=getstatscustomer.diffpartners,
        vendor_totalsales=getstatsvendor.totalsales,
        vendor_totalreviews=getstatsvendor.totalreviews,
        vendor_totaltrades=getstatsvendor.totaltrades,
        vendor_totalbtcrecieved=getstatsvendor.totalbtcrecieved,
        vendor_totalbtcspent=getstatsvendor.totalbtcspent,
        vendor_vendorrating=getstatsvendor.vendorrating,
        vendor_itemrating=getstatsvendor.avgitemrating,
    )

    if request.method == 'POST':
        if current_user.admin == 1:
            if getstatscustomer is not None:
                getstatscustomer.totalitemsbought = form.customer_totalitemsbought.data
                getstatscustomer.totalreviews = form.customer_totalreviews.data
                getstatscustomer.totaltrades = form.customer_totaltrades.data
                getstatscustomer.totalbtcrecieved = form.customer_totalbtcrecieved.data
                getstatscustomer.totalbtcspent = form.customer_totalbtcspent.data
                getstatscustomer.diffpartners = form.difftradingpartners.data

                getstatsvendor.totalsales = form.vendor_totalsales.data
                getstatsvendor.totalreviews = form.vendor_totalreviews.data
                getstatsvendor.totaltrades = form.vendor_totaltrades.data
                getstatsvendor.totalbtcrecieved = form.vendor_totalbtcrecieved.data
                getstatsvendor.totalbtcspent = form.vendor_totalbtcspent.data
                getstatsvendor.diffpartners = form.difftradingpartners.data
                getstatsvendor.avgitemrating = form.vendor_itemrating.data
                getstatsvendor.vendorrating = form.vendor_vendorrating.data

                db.session.add(getstatscustomer)
                db.session.add(getstatsvendor)

                db.session.commit()
                flash("Stats Updated", category="success")
                return redirect(url_for('admin.changeuser', username=username))
            else:
                flash("No user with that name", category="danger")
                return redirect(url_for('admin.changeuser', username=username))
        else:
            flash("Error", category="danger")
            return redirect(url_for('index', username=username))
    else:

        pass

    return render_template('admin/god/changeuser.html',
                           form=form,
                           getstatscustomer=getstatscustomer,
                           getstatsvendor=getstatsvendor,
                           username=username
                           )


@admin.route('/add-update/', methods=['GET', 'POST'])
@website_offline
@login_required
@ADMINaccount_required
def addupdate():
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    now = datetime.utcnow()
    updateform = addupdateform(request.form)
    title = 'Add an update'
    user = db.session.query(User).filter_by(
        username=current_user.username).first()
    if request.method == 'POST':
        if user.admin == 1:
            addanupdate = updateLog(
                header=updateform.title.data,
                body=updateform.description.data,
                dateofupdate=datetime.utcnow()
            )
            db.session.add(addanupdate)
            db.session.commit()
            flash("Added Update", category="success")
            return redirect(url_for('admin.addupdate'))
        else:
            flash("user not admin account", category="success")
    return render_template('admin/adddata/addupdate.html', user=user, now=now, updateform=updateform, title=title)


@admin.route('/account-management/', methods=['GET', 'POST'])
@website_offline
@login_required
@ADMINaccount_required
@ADMINaccountlevel10_required
def setaccounttoAdmin():
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    title = 'Admin Role'
    user = db.session.query(User).filter_by(
        username=current_user.username).first()
    adminform = settoAdmin(request.form)

    adminaccounts = db.session.query(User).filter_by(admin=1).all()
    if request.method == 'POST':
        if user.admin_role >= 5:
            finduser = db.session.query(User).filter_by(
                username=adminform.username.data).first()
            if finduser:
                finduser.admin = 1,
                finduser.admin_role = adminform.admin_role.data

                db.session.add(finduser)
                db.session.commit()
                return redirect(url_for('admin.setaccounttoAdmin'))
            else:
                flash("cant find username", category="danger")
        else:
            flash("user isnt high enough", category="danger")
    return render_template('admin/god/adminmanagement.html',
                           adminform=adminform,
                           title=title,
                           user=user,
                           adminaccounts=adminaccounts)


@admin.route('/add-achievement/', methods=['GET', 'POST'])
@website_offline
@login_required
@ADMINaccount_required
@ADMINaccountlevel10_required
def addAchievement():
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    achievementform = addachievement(request.form)
    title = 'Make a new Achievement'
    user = db.session.query(User).filter_by(
        username=current_user.username).first()
    if request.method == 'POST':
        if user.admin == 1:
            listof = achievementcategory()
            formdata = achievementform.category.data
            fulllist = dict(listof)
            name = fulllist[int(formdata)]

            addach = Achievements(
                categoryid=achievementform.achid.data,
                categoryname=name,
                value=achievementform.value.data,
                title=achievementform.title.data,
                description=achievementform.description.data,
            )
            db.session.add(addach)
            db.session.commit()
            flash("Achievement Added", category="success")
            return redirect(url_for('admin.addAchievement'))
        else:
            flash("user not admin account", category="success")
    return render_template('admin/adddata/achievement.html',
                           achievementform=achievementform,
                           title=title,
                           user=user)


@admin.route('/dispute/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@ADMINaccount_required
@ADMINaccountlevel3_required
def dispute(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    now = datetime.utcnow()
    postform = Chatform(request.form)
    disputeform = Disputeform(request.form)
    mod = db.session.query(User).filter_by(
        username=current_user.username).first()
    if current_user.is_authenticated:
        if mod.admin != 1:
            return redirect(url_for('index'))

    order = db.session.query(Orders).filter(Orders.id == id).first()

    posts = db.session.query(Chat)
    posts = posts.filter(Chat.orderid == order.id)
    posts = posts.filter(Chat.type == order.type)
    posts = posts.order_by(Chat.timestamp.desc())
    comments = posts.limit(50)

    # User
    user = db.session.query(User).filter_by(id=order.customer_id).first()
    usergetlevel = db.session.query(UserAchievements).filter_by(
        username=user.username).first()
    userpictureid = str(usergetlevel.level)
    userstats = db.session.query(StatisticsUser).filter_by(
        username=user.username).first()
    level = db.session.query(UserAchievements).filter_by(
        username=user.username).first()
    width = int(level.experiencepoints / 10)
    userreviews = db.session.query(Userreviews).filter(
        user.id == Userreviews.customer_id).limit(25)
    userach = db.session.query(whichAch).filter_by(user_id=user.id).first()

    # vendor
    vendor = db.session.query(User).filter_by(id=order.vendor_id).first()
    vendorstats = db.session.query(
        StatisticsVendor).filter_by(vendorid=vendor.id).first()
    vendorgetlevel = db.session.query(UserAchievements).filter_by(
        username=vendor.username).first()
    vendorpictureid = str(vendorgetlevel.level)
    vendorach = db.session.query(whichAch).filter_by(user_id=vendor.id).first()
    # vendorreviews
    vendorreviews = db.session.query(Feedback).filter(
        vendor.id == Feedback.vendorid).limit(25)

    if request.method == 'POST':
        if postform.post.data:
            # if they admin is chatting
            if order.type == 1:
                try:
                    post = Chat(
                        orderid=order.id,
                        author=current_user.username,
                        author_id=current_user.id,
                        timestamp=now,
                        body=postform.msgstufftosend.data,
                        admin=1,
                        type=1
                    )
                    db.session.add(post)
                    db.session.commit()

                    notification(type=19,
                                 username=order.customer,
                                 user_id=order.customer_id,
                                 salenumber=order.id,
                                 bitcoin=0)

                    notification(type=19,
                                 username=order.vendor,
                                 user_id=order.vendor_id,
                                 salenumber=order.id,
                                 bitcoin=0)

                except Exception as e:
                    print(str(e))

            return redirect(url_for('admin.dispute', id=id))

        # become mod of the issue
        if disputeform.start.data:
            order.modid = mod.id
            db.session.add(order)
            db.session.commit()

            return redirect(url_for('admin.dispute', id=id))

        if disputeform.one.data:
            # settle dispute
            # customers gets 100%

            cpercent = Decimal(1)

            # modify order
            order.completed = 1
            order.cancelled = 0
            order.new_order = 0
            order.accepted_order = 0
            order.disputed_order = 0
            order.waiting_order = 0
            order.delivered_order = 1

            # modify user
            user.dispute = 0
            vendor.dispute = 0

            db.session.add(user)
            db.session.add(order)
            db.session.add(vendor)
            db.session.commit()

            c = Decimal(order.price) * Decimal(cpercent)
            x = Decimal(order.shipping_price)
            whole_price = c + x
            if order.type == 1:

                btc_cash_sendCointoUser(amount=whole_price,
                                        comment=order.id,
                                        user_id=order.customer_id
                                        )

                flash("Trade has been decided. 100/0 split", category="danger")
                return redirect(url_for('admin.dispute', id=id))

            else:

                flash("100/0 ERROR", category="danger")
                return redirect(url_for('admin.dispute', id=id))

        if disputeform.two.data:
            # settle dispute
            # customers gets 75%
            cpercent = Decimal(0.75)
            vpercent = Decimal(0.25)

            # modify order
            order.completed = 1
            order.cancelled = 0
            order.new_order = 0
            order.accepted_order = 0
            order.disputed_order = 0
            order.waiting_order = 0
            order.delivered_order = 1

            # modify user
            user.dispute = 0
            vendor.dispute = 0

            db.session.add(user)
            db.session.add(order)
            db.session.add(vendor)

            db.session.commit()

            c = Decimal(order.price) * Decimal(cpercent)
            vnofee = Decimal(order.price) * Decimal(vpercent)

            vendor_withshipping = Decimal(
                vnofee) + (Decimal(vpercent) * Decimal(order.shipping_price))
            customer_withshipping = Decimal(
                c) + (Decimal(cpercent) * Decimal(order.shipping_price))

            if order.type == 1:

                if order.digital_currency == 3:
                    btc_cash_sendCointoUser(amount=customer_withshipping,
                                            comment=order.id,
                                            user_id=order.customer_id,
                                            )

                    btc_cash_sendCointoUser(amount=vendor_withshipping,
                                            comment=order.id,
                                            user_id=order.vendor_id,
                                            )
            else:
                pass

            flash("Trade has been decided. 75/25 split", category="danger")
            return redirect(url_for('admin.dispute', id=id))

        # Customer 50
        #  vendor 50
        ##
        if disputeform.three.data:

            cpercent = Decimal(0.50)
            vpercent = Decimal(0.50)

            # modify order
            order.completed = 1
            order.cancelled = 0
            order.new_order = 0
            order.accepted_order = 0
            order.disputed_order = 0
            order.waiting_order = 0
            order.delivered_order = 1

            # modify user
            user.dispute = 0
            vendor.dispute = 0

            db.session.add(user)
            db.session.add(order)
            db.session.add(vendor)
            db.session.commit()

            c = Decimal(order.price) * Decimal(cpercent)
            vnofee = Decimal(order.price) * Decimal(vpercent)

            vendor_withshipping = Decimal(
                vnofee) + (Decimal(vpercent) * Decimal(order.shipping_price))
            customer_withshipping = Decimal(
                c) + (Decimal(cpercent) * Decimal(order.shipping_price))

            if order.type == 1:

                btc_cash_sendCointoUser(amount=customer_withshipping,
                                        comment=order.id,
                                        user_id=order.customer_id,
                                        )

                btc_cash_sendCointoUser(amount=vendor_withshipping,
                                        comment=order.id,
                                        user_id=order.vendor_id,
                                        )

            else:
                pass

            flash("Trade has been decided. 50/50 split", category="danger")
            return redirect(url_for('admin.dispute', id=id))

        # Customer 25
        #  vendor 75
        ##
        if disputeform.four.data:
            # customers gets 25%
            cpercent = Decimal(0.25)
            vpercent = Decimal(0.75)

            # modify order
            order.completed = 1
            order.cancelled = 0
            order.new_order = 0
            order.accepted_order = 0
            order.waiting_order = 0
            order.delivered_order = 1
            order.disputed_order = 0

            # modify user
            user.dispute = 0
            vendor.dispute = 0

            db.session.add(vendor)
            db.session.add(order)
            db.session.add(user)
            db.session.commit()

            c = Decimal(order.price) * Decimal(cpercent)
            vnofee = Decimal(order.price) * Decimal(vpercent)

            vendor_withshipping = Decimal(
                vnofee) + (Decimal(vpercent) * Decimal(order.shipping_price))
            customer_withshipping = Decimal(
                c) + (Decimal(cpercent) * Decimal(order.shipping_price))

            if order.type == 1:

                btc_cash_sendCointoUser(amount=customer_withshipping,
                                        comment=order.id,
                                        user_id=order.customer_id,
                                        )

                btc_cash_sendCointoUser(amount=vendor_withshipping,
                                        comment=order.id,
                                        user_id=order.vendor_id,
                                        )

            flash("Trade has been decided. 25/75 split", category="danger")
            return redirect(url_for('admin.dispute', id=id))

        # Customer 0
        #  vendor 100
        ##
        if disputeform.five.data:

            # modify order
            order.completed = 1
            order.new_order = 0
            order.accepted_order = 0
            order.cancelled = 0
            order.waiting_order = 0
            order.delivered_order = 1
            order.disputed_order = 0

            # modify user
            user.dispute = 0
            vendor.dispute = 0

            db.session.add(user)
            db.session.add(vendor)
            db.session.add(order)
            db.session.commit()

            c = Decimal(order.price)
            x = Decimal(order.shipping_price)
            whole_price = c + x

            if order.type == 1:

                btc_cash_sendCointoUser(amount=whole_price,
                                        comment=order.id,
                                        user_id=order.vendor_id,
                                        )

            flash("Trade has been decided. 0/100 split", category="danger")
            return redirect(url_for('admin.dispute', id=id))

        # UNDISPUTE
        #
        if disputeform.undispute.data:
            # modify order
            order.disputed_order = 0
            user.dispute = 0
            vendor.dispute = 0

            db.session.add(order)
            db.session.add(user)
            db.session.add(vendor)
            db.session.commit()

            flash("Undisputed Order", category="danger")
            return redirect(url_for('admin.dispute', id=id))

        if disputeform.addtime1.data:
            # if item purchase

            td = timedelta(hours=24)
            newreturnby = order.return_by + td
            newreturncancelage = order.returncancelage
            order.return_by = newreturnby
            order.returncancelage = newreturncancelage
            db.session.add(order)
            db.session.commit()

            flash("Added 24 hours", category="danger")
            return redirect(url_for('admin.dispute', id=id))

        if disputeform.addtimetwodays.data:
            # if item purchase
            if order.type == 1:
                td = timedelta(hours=48)
                newreturnby = order.return_by + td
                newreturncancelage = order.returncancelage

                order.return_by = newreturnby
                order.returncancelage = newreturncancelage
                db.session.add(order)
                db.session.commit()
            else:
                return redirect(url_for('admin.adminHome'))

            flash("Added 48 hours", category="danger")
            return redirect(url_for('admin.dispute', id=id))

        if disputeform.addtimeweek.data:

            # if item purcha
            td = timedelta(days=7)
            newreturnby = order.return_by + td
            newreturncancelage = order.returncancelage

            order.return_by = newreturnby
            order.returncancelage = newreturncancelage
            db.session.add(order)
            db.session.commit()

            flash("Added One Week", category="danger")
            return redirect(url_for('admin.dispute', id=id))

        if disputeform.abortorder.data:
            item = db.session.query(Orders).filter_by(id=id).first()
            msg = db.session.query(
                shippingSecret).filter_by(orderid=id).first()
            gettracking = db.session.query(
                Tracking).filter_by(sale_id=id).first()
            if item.completed == 0:
                try:
                    item.cancelled = 1
                    item.completed = 1
                    item.released = 0
                    item.completed_time = now
                    item.disputed_order = 0
                    item.waiting_order = 0
                    item.delivered_order = 0
                    item.new_order = 0
                    item.accepted_order = 0
                    item.request_cancel = 0

                    db.session.add(item)
                    db.session.commit()

                    # calculate how much to refund(shipping and price)
                    p = item.price
                    s = item.shipping_price
                    if s:
                        s = s
                    else:
                        s = 0
                    refund = Decimal(p) + Decimal(s)

                    btc_cash_sendCointoUser(amount=refund,
                                            comment=item.id,
                                            user_id=item.customer_id,
                                            )

                    if msg:
                        db.session.delete(msg)
                        db.session.commit()
                    else:
                        pass

                    if gettracking:
                        db.session.delete(gettracking)
                        db.session.commit()
                    else:
                        pass

                    notification(type=7,
                                 username=item.customer,
                                 user_id=item.customer_id,
                                 salenumber=item.id,
                                 bitcoin=0)

                    flash("Order Cancelled", category="danger")
                    return redirect(url_for('admin.dispute', id=id))
                except Exception as e:
                    flash("Error", category="danger")
                    return redirect(url_for('admin.dispute', id=id))
            else:
                flash(
                    "Error. Order completed already..Might be trying to get scammed....", category="danger")
                return redirect(url_for('admin.dispute', id=id))
        else:
            return redirect(url_for('admin.adminHome'))

    return render_template('admin/dispute.html',
                           user=user, now=now,
                           vendor=vendor,
                           order=order,
                           usergetlevel=usergetlevel,
                           userpictureid=userpictureid,
                           vendorstats=vendorstats,
                           vendorgetlevel=vendorgetlevel,
                           vendorpictureid=vendorpictureid,
                           postform=postform,
                           comments=comments,
                           disputeform=disputeform,
                           vendorreviews=vendorreviews,
                           userreviews=userreviews,
                           level=level,
                           width=width,
                           userstats=userstats,
                           userach=userach,
                           vendorach=vendorach
                           )


@admin.route('/msg/<int:id>', methods=['GET', 'POST'])
@ping_user
@website_offline
@login_required
@ADMINaccount_required
@ADMINaccountlevel3_required
def messenger(id):

    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    now = datetime.utcnow()

    postform = Chatform(request.form)
    # User

    # themsg
    msg = db.session.query(PostUser)
    msg = msg.filter_by(id=id).first()

    # comments
    comments = db.session.query(Comment)
    comments = comments.filter(Comment.post_id == msg.postid)
    comments = comments.order_by(Comment.timestamp.desc())
    comments = comments.all()

    # user
    user = db.session.query(User).filter_by(
        username=current_user.username).first()
    usergetlevel = db.session.query(UserAchievements).filter_by(
        username=user.username).first()
    userpictureid = str(usergetlevel.level)
    userstats = db.session.query(StatisticsUser).filter_by(
        username=user.username).first()
    level = db.session.query(UserAchievements).filter_by(
        username=user.username).first()
    width = int(level.experiencepoints / 10)
    userach = db.session.query(whichAch).filter_by(user_id=user.id).first()

    # vendor
    vendor = db.session.query(User).filter_by(id=msg.author_id).first()
    vendorstats = db.session.query(
        StatisticsVendor).filter_by(vendorid=vendor.id).first()
    vendorgetlevel = db.session.query(UserAchievements).filter_by(
        username=vendor.username).first()
    vendorpictureid = str(vendorgetlevel.level)
    vendorach = db.session.query(whichAch).filter_by(user_id=vendor.id).first()

    if request.method == 'POST':
        if user.admin == 1:
            if postform.post.data:
                post = Comment(
                    author_id=current_user.id,
                    author=current_user.username,
                    timestamp=datetime.utcnow(),
                    body=postform.msgstufftosend.data,
                    post_id=msg.postid,
                    modid=current_user.id
                )
                db.session.add(post)
                db.session.commit()

                getpost = db.session.query(PostUser)
                getpost = getpost.filter(PostUser.postid == msg.postid)
                getallposts = getpost.all()

                for f in getallposts:
                    f.unread = 1
                    f.modid = current_user.id
                    f.official = 1
                    db.session.add(f)
                    db.session.commit()

                return redirect(url_for('admin.messenger', id=msg.id))

    return render_template('admin/messenger.html',
                           user=user, now=now,
                           userpictureid=userpictureid,
                           userstats=userstats,
                           level=level,
                           width=width,
                           usergetlevel=usergetlevel,
                           vendor=vendor,
                           vendorstats=vendorstats,
                           vendorgetlevel=vendorgetlevel,
                           vendorpictureid=vendorpictureid,
                           msg=msg,
                           postform=postform,
                           comments=comments,
                           userach=userach,
                           vendorach=vendorach
                           )


@admin.route('/dispute/becomeadmin/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ADMINaccount_required
@ADMINaccountlevel10_required
def order_becomeadmin(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    getorder = db.session.query(Orders).filter_by(id=id).first()
    getorder.modid = current_user.id
    db.session.add(getorder)
    db.session.commit()
    return redirect(url_for('admin.adminHome', username=current_user.username))


@admin.route('/msg/becomeadmin/<int:id>', methods=['GET', 'POST'])
@website_offline
@ADMINaccount_required
@ADMINaccountlevel3_required
def msg_dispute_becomeadmin(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    getpost = db.session.query(PostUser).filter_by(id=id).first()
    getpost.modid = current_user.id
    db.session.add(getpost)
    db.session.commit()
    return redirect(url_for('admin.adminHome', username=current_user.username))


@admin.route('/msg/settlemsg/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ADMINaccountlevel3_required
def msg_dispute_settle(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    getpost = db.session.query(PostUser).filter_by(id=id).first()
    getpost.official = 0
    db.session.add(getpost)
    db.session.commit()
    return redirect(url_for('admin.adminHome', username=current_user.username))


@admin.route('/msg/delete/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ADMINaccountlevel3_required
def msg_delete(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    getpost = db.session.query(PostUser).filter_by(id=id).first()
    db.session.delete(getpost)
    db.session.commit()
    comments = db.session.query(Comment).filter(Comment.post_id == id).all()
    if comments:
        for f in comments:
            db.session.delete(f)
            db.session.commit()
    return redirect(url_for('admin.adminHome', username=current_user.username))


@admin.route('/feedback/delete/<int:id>', methods=['GET', 'POST'])
@website_offline
@ADMINaccount_required
@ADMINaccountlevel3_required
def feedback_delete(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    getpost = db.session.query(websitefeedback).filter_by(id=id).first()
    db.session.delete(getpost)
    db.session.commit()
    return redirect(url_for('admin.adminHome', username=current_user.username))


@admin.route('/clearnetprofit/', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel10_required
def admin_clearnetprofit():
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    now = datetime.utcnow()
    user = db.session.query(User).filter_by(id=current_user.id).first()
    if user.admin_role > 5:
        # pagination
        search = False
        q = request.args.get('q')
        if q:
            search = True
        page, per_page, offset = get_page_args()
        # PEr Page tells how many search results pages
        inner_window = 1  # search bar at bottom used for .. lots of pages
        outer_window = 1  # search bar at bottom used for .. lots of pages
        per_page = 1000
        # Get Transaction history

        transactfull = db.session.query(clearnetprofit_btc)
        transactfull = transactfull.order_by(
            clearnetprofit_btc.timestamp.desc())

        transactcount = transactfull.count()
        profita = transactfull.limit(per_page).offset(offset)

        pagination = Pagination(page=page,
                                total=transactfull.count(),
                                search=search,
                                record_name='items',
                                offset=offset,
                                per_page=per_page,
                                css_framework='bootstrap4',
                                inner_window=inner_window,
                                outer_window=outer_window)

        return render_template('admin/god/profit.html',
                               user=user, now=now,
                               transactcount=transactcount,
                               pagination=pagination,
                               profita=profita,
                               )
    else:
        return redirect(url_for('index'))


@admin.route('/viewflaggeditems/', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel3_required
def viewflaggeditems():

    items = db.session.query(flagged)
    items = items.order_by(flagged.howmany.desc())
    item = items.all()
    countitem = items.count()
    return render_template('admin/viewflaggeditems.html',
                           item=item,
                           countitem=countitem
                           )


@admin.route('/removeflags/<int:id>', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel3_required
def removeflags(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    getflaggeditem = db.session.query(flagged).filter_by(id=id).first()
    db.session.delete(getflaggeditem)
    db.session.commit()
    flash("Flags Deleted", category="warning")
    return redirect(url_for('admin.viewflaggeditems'))


@admin.route('/deletevendoritem/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@ADMINaccount_required
@ADMINaccountlevel3_required
def deleteItem(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    import os
    from app import UPLOADED_FILES_DEST
    ext1 = '_100x100_fit_85'
    ext2 = '_125x125_fit_85'
    ext3 = '_200x200_fit_85'
    global file10
    global file11
    global file12
    global file13

    global file20
    global file21
    global file22
    global file23

    global file30
    global file31
    global file32
    global file33

    global file40
    global file41
    global file42
    global file43

    global file50
    global file51
    global file52
    global file53
    global pathtofile1
    global file_extension1
    global pathtofile2
    global file_extension2

    global pathtofile3
    global file_extension3

    global pathtofile4
    global file_extension4

    global pathtofile5
    global file_extension5
    item = marketItem.query.get(id)

    try:
        specific_folder = str(item.id)

        link = 'item'
        spacer = '/'
        pathtofile1 = str(UPLOADED_FILES_DEST + spacer + link + spacer +
                          specific_folder + spacer + item.imageone)
        pathtofile2 = str(UPLOADED_FILES_DEST + spacer + link + spacer +
                          specific_folder + spacer + item.imagetwo)
        pathtofile3 = str(UPLOADED_FILES_DEST + spacer + link + spacer +
                          specific_folder + spacer + item.imagethree)
        pathtofile4 = str(UPLOADED_FILES_DEST + spacer + link + spacer +
                          specific_folder + spacer + item.imagefour)
        pathtofile5 = str(UPLOADED_FILES_DEST + spacer + link + spacer +
                          specific_folder + spacer + item.imagefive)

        try:

            pathtofile1, file_extension1 = os.path.splitext(pathtofile1)
        except:
            pass
        try:

            pathtofile2, file_extension2 = os.path.splitext(pathtofile2)
        except:
            pass
        try:

            pathtofile3, file_extension3 = os.path.splitext(pathtofile3)
        except:
            pass
        try:

            pathtofile4, file_extension4 = os.path.splitext(pathtofile4)
        except:
            pass
        try:

            pathtofile5, file_extension5 = os.path.splitext(pathtofile5)
        except:
            pass

        try:
            file10 = str(pathtofile1 + file_extension1)
            file11 = str(pathtofile1 + ext1 + file_extension1)
            file12 = str(pathtofile1 + ext2 + file_extension1)
            file13 = str(pathtofile1 + ext3 + file_extension1)
        except:
            pass

        try:
            file20 = str(pathtofile2 + file_extension2)
            file21 = str(pathtofile2 + ext1 + file_extension2)
            file22 = str(pathtofile2 + ext2 + file_extension2)
            file23 = str(pathtofile2 + ext3 + file_extension2)
        except:
            pass

        try:
            file30 = str(pathtofile3 + file_extension3)
            file31 = str(pathtofile3 + ext1 + file_extension3)
            file32 = str(pathtofile3 + ext2 + file_extension3)
            file33 = str(pathtofile3 + ext3 + file_extension3)
        except:
            pass

        try:
            file40 = str(pathtofile4 + file_extension4)
            file41 = str(pathtofile4 + ext1 + file_extension4)
            file42 = str(pathtofile4 + ext2 + file_extension4)
            file43 = str(pathtofile4 + ext3 + file_extension4)
        except:
            pass

        try:
            file50 = str(pathtofile5 + file_extension5)
            file51 = str(pathtofile5 + ext1 + file_extension5)
            file52 = str(pathtofile5 + ext2 + file_extension5)
            file53 = str(pathtofile5 + ext3 + file_extension5)
        except:
            pass

        x1 = item.imageone
        if len(x1) > 10:
            try:
                os.remove(file10)
            except:
                pass
            try:
                os.remove(file11)
            except:
                pass
            try:
                os.remove(file12)
            except:
                pass
            try:
                os.remove(file13)
            except:
                pass
        else:
            pass
        x2 = item.imagetwo
        if len(x2) > 10:
            try:
                os.remove(file20)
            except:
                pass
            try:
                os.remove(file21)
            except:
                pass
            try:
                os.remove(file22)
            except:
                pass
            try:
                os.remove(file23)
            except:
                pass
        else:
            pass
        x3 = item.imagethree
        if len(x3) > 10:
            try:
                os.remove(file30)
            except:
                pass
            try:
                os.remove(file31)
            except:
                pass
            try:
                os.remove(file32)
            except:
                pass
            try:
                os.remove(file33)
            except:
                pass
        else:
            pass
        x4 = item.imagefour
        if len(x4) > 10:
            try:
                os.remove(file40)
            except:
                pass
            try:
                os.remove(file41)
            except:
                pass
            try:
                os.remove(file42)
            except:
                pass
            try:
                os.remove(file43)
            except:
                pass
        else:
            pass
        x5 = item.imagefive
        if len(x5) > 10:
            try:
                os.remove(file50)
            except:
                pass
            try:
                os.remove(file51)
            except:
                pass
            try:
                os.remove(file52)
            except:
                pass
            try:
                os.remove(file53)
            except:
                pass
        else:
            pass
        db.session.delete(item)
        db.session.commit()
        flash("Item Deleted", category="success")
        return redirect(url_for('admin.viewflaggeditems'))
    except Exception:
        flash("Error", category="danger")
        return redirect(url_for('admin.viewflaggeditems'))


@admin.route('/admin/viewuser/<username>', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel3_required
def admin_viewuser(username):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    form = Userform()
    now = datetime.utcnow()

    # Pagination
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()
    # PEr Page tells how many search results pages
    inner_window = 1  # search bar at bottom used for .. lots of pages
    outer_window = 1  # search bar at bottom used for .. lots of pages
    per_page = 10
    # End Pagination

    user = db.session.query(User).filter_by(username=username).first()
    if user is not None:
        userwallet = db.session.query().filter_by(user_id=user.id).first()

        # Get Transaction history
        transactfull = db.session.query(TransactionsBch)
        transactfull = transactfull.filter(TransactionsBch.user_id == user.id)
        transactfull = transactfull.order_by(TransactionsBch.id.desc())
        transactcount = transactfull.count()
        transact = transactfull.limit(per_page).offset(offset)

        pagination = Pagination(page=page,
                                total=transactfull.count(),
                                search=search,
                                record_name='items',
                                offset=offset,
                                per_page=per_page,
                                css_framework='bootstrap4',
                                inner_window=inner_window,
                                outer_window=outer_window)
        if request.method == 'POST':
            if user.admin == 1:
                if form.lockwallet.data:
                    userwallet.locked = 1
                    flash("Wallet Locked",
                          category="danger")
                elif form.unlockwallet.data:
                    userwallet.locked = 0

                elif form.selectshardsubmit.data:
                    theshard = form.selectshard.data
                    shard = theshard.value

                    user.shard = shard
                    userwallet.shard = shard
                    userwallet.address1 = ''
                    userwallet.address2 = ''
                    userwallet.address3 = ''
                    userwallet.address1status = 0
                    userwallet.address2status = 0
                    userwallet.address3status = 0
                    db.session.add(user)
                    db.session.add(userwallet)
                    db.session.commit()
                    flash("User has new shard",
                          category="success")

                db.session.add(userwallet)
                db.session.commit()

        return render_template('admin/viewid/viewuser.html',
                               user=user,
                               now=now,
                               userwallet=userwallet,
                               form=form,
                               transactcount=transactcount,
                               transact=transact,
                               pagination=pagination


                               )
    else:
        flash("User doesnt exist. Check spelling", category="danger")
        return redirect(url_for('admin.adminHome'))


@admin.route('/admin/movemoney', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel10_required
def admin_movemoney():
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    title = 'Send money from user'
    form = adminsendMoney()
    now = datetime.utcnow()

    user = db.session.query(User).filter_by(id=current_user.id).first()
    userwallet = db.session.query(BchWallet).filter_by(user_id=user.id).first()

    if request.method == 'POST':
        if user.admin == 1:
            sendto = form.sendto.data
            description = form.description.data
            amount = form.amount.data

            finduser = db.session.query(User).filter(
                User.username == sendto).first()
            if finduser:
                theuser = finduser.id
                theusername = str(finduser.username)
                theuser_id = str(finduser.id)

                if form.submit.data:
                    if current_user.admin_role == 10:
                        btc_cash_send_coin_to_user_as_admin(
                            amount=amount, comment=description, user_id=theuser)
                        flash("Money sent to: " + theusername + " with user id: " + theuser_id,
                              category="success")
                        return redirect(url_for('admin.admin_movemoney'))
                    else:
                        return redirect(url_for('index', username=current_user.username))
                else:
                    return redirect(url_for('index', username=current_user.username))

            else:

                flash("User doesnt exist",
                      category="danger")
                return redirect(url_for('admin.admin_movemoney'))
    return render_template('admin/god/movemoney.html',
                           user=user,
                           now=now,
                           userwallet=userwallet,
                           form=form,
                           title=title
                           )


@admin.route('/admin/movemoneyfromuser', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel10_required
def admin_movemoney_fromuser():
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    title = 'Take money from user'
    form = adminsendMoney()
    now = datetime.utcnow()

    user = db.session.query(User).filter_by(id=current_user.id).first()
    userwallet = db.session.query(BchWallet).filter_by(user_id=user.id).first()

    if request.method == 'POST':
        if user.admin == 1:
            sendto = form.sendto.data
            description = form.description.data
            amount = form.amount.data

            finduser = db.session.query(User).filter(
                User.username == sendto).first()
            if finduser:
                theuser = finduser.id
                theusername = str(finduser.username)
                theuser_id = str(finduser.id)

                if form.submit.data:
                    if current_user.admin_role == 10:
                        btc_cash_send_coin_to_user_as_admin(amount=amount,
                                                            comment=description,
                                                            user_id=theuser)

                        flash("Money taken from : " + theusername + " with user id: " + theuser_id,
                              category="success")
                        return redirect(url_for('admin.admin_movemoney_fromuser'))
                    else:
                        return redirect(url_for('index', username=current_user.username))
                else:
                    return redirect(url_for('index', username=current_user.username))
            else:
                flash("User doesnt exist",
                      category="danger")
                return redirect(url_for('admin.admin_movemoney_fromuser'))

    return render_template('admin/god/movemoney.html',
                           user=user,
                           now=now,
                           userwallet=userwallet,
                           form=form,
                           title=title
                           )


@admin.route('/admin/viewitem/<int:id>', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel3_required
def admin_viewitem(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    now = datetime.utcnow()
    user = db.session.query(User).filter_by(
        username=current_user.username).first()
    getitem = db.session.query(marketItem).filter_by(id=id).first()
    return render_template('admin/viewid/viewitem.html',
                           user=user, now=now,
                           getitem=getitem)


@admin.route('/vieworder/<int:id>', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel3_required
def admin_vieworder(id):
    if current_user.is_authenticated:
        if current_user.admin == 0:
            return redirect(url_for('index'))
        else:
            pass
    now = datetime.utcnow()
    user = db.session.query(User).filter_by(
        username=current_user.username).first()
    order = db.session.query(Orders).filter_by(id=id).first()
    if order is None:

        flash("Order has been deleted.", category="success")
        return redirect(url_for('index', username=current_user.username))

    item = db.session.query(marketItem).filter(
        marketItem.id == order.item_id).first()

    transactfull = db.session.query(TransactionsBch)
    transactfull = transactfull.filter(TransactionsBch.commentbtc == str(id))
    transactfull = transactfull.order_by(TransactionsBch.timeoft.asc())
    transactcount = transactfull.count()
    transact = transactfull.all()

    return render_template('admin/viewid/vieworder.html',
                           user=user, now=now,
                           order=order,
                           item=item,
                           transact=transact, transactcount=transactcount)


@admin.route('/viewadminorders', methods=['GET', 'POST'])
@ADMINaccount_required
@ADMINaccountlevel3_required
def admin_viewallorders():

    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()
    # PEr Page tells how many search results pages
    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 10

    ordernew1 = db.session.query(Orders).filter(Orders.new_order == 1,
                                                Orders.completed == 0,
                                                Orders.type == 1
                                                )
    ordernew1 = ordernew1.order_by(Orders.id.desc())
    ordernew = ordernew1.limit(per_page).offset(offset)
    ordernewcount = ordernew1.count()

    paginationordernew = Pagination(page=page,
                                    total=ordernew1.count(),
                                    search=search,
                                    record_name='items',
                                    offset=offset,
                                    per_page=per_page,
                                    css_framework='bootstrap5',
                                    inner_window=inner_window,
                                    outer_window=outer_window)

    orderaccepted1 = db.session.query(Orders).filter(Orders.accepted_order == 1,
                                                     Orders.completed == 0,
                                                     Orders.type == 1
                                                     )

    orderaccepted1 = orderaccepted1.order_by(Orders.id.desc())
    orderaccepted = orderaccepted1.limit(per_page).offset(offset)
    orderacceptedcount = orderaccepted1.count()
    paginationorderaccepted = Pagination(page=page,
                                         total=orderaccepted1.count(),
                                         search=search,
                                         record_name='items',
                                         offset=offset,
                                         per_page=per_page,
                                         css_framework='bootstrap4',
                                         inner_window=inner_window,
                                         outer_window=outer_window)

    orderwaiting1 = db.session.query(Orders).filter(Orders.waiting_order == 1,
                                                    Orders.completed == 0,
                                                    Orders.type == 1
                                                    )

    orderwaiting1 = orderwaiting1.order_by(Orders.id.desc())
    orderwaiting = orderwaiting1.limit(per_page).offset(offset)
    orderwaitingcount = orderwaiting1.count()
    paginationorderwaiting = Pagination(page=page,
                                        total=orderwaiting1.count(),
                                        search=search,
                                        record_name='items',
                                        offset=offset,
                                        per_page=per_page,
                                        css_framework='bootstrap4',
                                        inner_window=inner_window,
                                        outer_window=outer_window)

    completed1 = db.session.query(Orders).filter(Orders.completed == 1,
                                                 Orders.type == 1
                                                 )

    completed1 = completed1.order_by(Orders.id.desc())
    completed = completed1.limit(per_page).offset(offset)
    completedcount = completed1.count()
    paginationcompleted = Pagination(page=page,
                                     total=completed1.count(),
                                     search=search,
                                     record_name='items',
                                     offset=offset,
                                     per_page=per_page,
                                     css_framework='bootstrap4',
                                     inner_window=inner_window,
                                     outer_window=outer_window)

    return render_template('/admin/itemmanagement/viewallorders.html',
                           completed=completed,
                           ordernew=ordernew,
                           orderaccepted=orderaccepted,
                           orderwaiting=orderwaiting,
                           ordernewcount=ordernewcount,
                           orderacceptedcount=orderacceptedcount,
                           orderwaitingcount=orderwaitingcount,
                           completedcount=completedcount,
                           paginationordernew=paginationordernew,
                           paginationorderaccepted=paginationorderaccepted,
                           paginationorderwaiting=paginationorderwaiting,
                           paginationcompleted=paginationcompleted,
                           )
