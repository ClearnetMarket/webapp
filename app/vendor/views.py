from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.vendor import vendor

from decimal import Decimal
from sqlalchemy import func
from flask_paginate import Pagination, get_page_args
from app.exppoints import exppoint
from app.common.decorators import \
    website_offline, \
    login_required, \
    vendoraccount_required

# forms
from app.vendor.forms import \
    ratingsForm, \
    feedbackcomment, \
    addtempreturn, \
    vendorleavereview, \
    addShipping

from app.userdata.views import \
    userdata_add_total_items_bought, \
    addtotalItemsSold, \
    userdata_different_trading_partners_user, \
    userdata_different_trading_partners_vendor, \
    userdata_total_spent_on_item_bch, \
    userdata_total_made_on_item_bch
from app.search.searchfunction import headerfunctions_vendor
from app.notification import notification

from app.search.searchfunction import headerfunctions_vendor
from app.wallet_bch.wallet_btccash_work import \
    btc_cash_sendCointoclearnet, \
    btc_cash_sendCointoUser

from app.auth.forms import becomeavendor

# models
from app.classes.auth import Auth_User

from app.classes.item import Item_MarketItem

from app.classes.profile import \
    Profile_Userreviews, \
    Profile_FeedbackComments

from app.classes.service import \
    Service_ShippingSecret, \
    Service_Returns, \
    Service_ReturnsTracking, \
    Service_DefaultReturns, \
    Service_Tracking

from app.classes.userdata import \
    User_DataFeedback

from app.classes.vendor import \
    Vendor_Orders

from app.classes.wallet_bch import *
# End Models


@vendor.route('/sell', methods=['GET', 'POST'])
@website_offline
@login_required
def vendor_become_vendor():
    if current_user.vendor_account == 0:
        form = becomeavendor(request.form)
        if request.method == 'POST':
            return redirect(url_for('auth.setup_account'))
        return render_template('auth/account/vendorintro.html', form=form)
    else:
        return redirect(url_for('vendorcreate.vendorcreate_sell_options', username=current_user.username))


@vendor.route('/vendor-accept/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders_accept(id):
    try:
        item = Vendor_Orders.query.get(id)
        if item is not None:
            if item.vendor_id == current_user.id and item.vendor_id != 0 and item.released == 0:
                try:
                    item.new_order = 0
                    item.accepted_order = 1
                    item.age = datetime.utcnow()
                    item.age
                    db.session.add(item)
                    db.session.commit()
                    flash("Order Accepted", category="success")
                    return redirect(url_for('vendor.vendor_orders', username=current_user.username))
                except Exception:
                    return redirect(url_for('vendor.vendor_orders', username=current_user.username))
            else:
                return redirect(url_for('vendor.vendor_orders', username=current_user.username))
        else:
            flash("Error.  Item doesnt exist", category="danger")
            return redirect(url_for('index'))

    except:
        return redirect(url_for('index', username=current_user.username))


@vendor.route('/vendor-send/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders_send(id):
    try:
        item = Vendor_Orders.query.get(id)
        if item:
            if item.vendor_id == current_user.id \
                    and item.vendor_id != 0 \
                    and item.released == 0:
                try:
                    item.accepted_order = 0
                    item.request_cancel = 0
                    item.waiting_order = 1
                    item.reason_cancel = 0
                    db.session.add(item)
                    db.session.commit()
                    flash("Order Shipped", category="success")
                    return redirect(url_for('vendor.vendor_orders', username=current_user.username))
                except Exception:
                    return redirect(url_for('vendor.vendor_orders', username=current_user.username))
            else:
                return redirect(url_for('vendor.vendor_orders', username=current_user.username))
        else:
            flash("Error", category="danger")
            return redirect(url_for('index'))

    except:
        return redirect(url_for('index', username=current_user.username))


@vendor.route('/vendor-dispute/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders_disput(id):
    try:
        item = Vendor_Orders.query.get(id)
        if item.vendor_id == current_user.id:
            try:
                item.disputed_order = 1
                db.session.add(item)
                db.session.commit()
                flash("Item Disputed", category="success")
                return redirect(url_for('customerservice.customerservice_dispute', username=current_user.username))
            except Exception:
                return redirect(url_for('customerservice.customerservice_dispute', username=current_user.username))
        else:
            return redirect(url_for('customerservice.customerservice_dispute', username=current_user.username))
    except:
        return redirect(url_for('index', username=current_user.username))


@vendor.route('/customer-dispute/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders_customer_dispute(id):
    item = Vendor_Orders.query.get(id)
    if item:
        try:
            if item.vendor_id == current_user.id or item.customer_id == current_user.id:
                item.disputed_order = 1
                db.session.add(item)
                db.session.commit()
                flash("Item Disputed", category="success")
                return redirect(url_for('customerservice.customerservice_dispute', username=current_user.username))
            else:
                return redirect(url_for('index', username=current_user.username))
        except:
            return redirect(url_for('index', username=current_user.username))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-reject/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders_reject(id):
    now = datetime.utcnow()
    item = Vendor_Orders.query.get(id)
    if item:
        try:
            msg = db.session\
                .query(Service_ShippingSecret)\
                .filter_by(orderid=id)\
                .first()
            gettracking = db.session\
                .query(Service_Tracking)\
                .filter_by(sale_id=id)\
                .first()
            if item.vendor_id == current_user.id and item.released == 0 and item.vendor_id != 0:
                if item.completed == 0:
                    try:
                        item.cancelled = 1
                        item.completed = 1
                        item.completed_time = now
                        item.disputed_order = 0
                        item.request_cancel = 0
                        item.waiting_order = 0
                        item.delivered_order = 0
                        item.new_order = 0
                        item.accepted_order = 0

                        db.session.add(item)
                        db.session.flush()

                        # calculate how much to refund(shipping and price)
                        the_item_price = item.price
                        the_item_shipping_price = item.shipping_price
                        if the_item_shipping_price:
                            the_item_shipping_price = the_item_shipping_price
                        else:
                            the_item_shipping_price = 0
                        refund = Decimal(the_item_price) + \
                            Decimal(the_item_shipping_price)

                        btc_cash_sendCointoUser(amount=refund,
                                                comment=item.id,
                                                user_id=item.vendor_id,
                                                )
                        # delete shipping message
                        if msg:
                            db.session.delete(msg)
                        # delete tracking
                        if gettracking:
                            db.session.delete(gettracking)
                        # change the quantity
                        if item.type == 1:
                            getitem = db.session.query(Item_MarketItem).filter(
                                item.item_id == Item_MarketItem.id).first()
                            x = getitem.item_count
                            y = item.quantity
                            z = x + y
                            getitem.item_count = z
                            db.session.add(getitem)

                        notification(type=7, username=item.customer,
                                     user_id=item.customer_id, salenumber=item.id, bitcoin=0)
                        flash("Order Cancelled", category="danger")
                        db.session.commit()
                        return redirect(url_for('vendor.vendor_orders', username=current_user.username))
                    except Exception as e:
                        flash("Error", category="danger")
                        return redirect(url_for('vendor.vendor_orders', username=current_user.username))
                else:
                    flash("Error", category="danger")
                    return redirect(url_for('vendor.vendor_orders', username=current_user.username))
            else:
                return redirect(url_for('vendor.vendor_orders', username=current_user.username))
        except Exception as e:
            return redirect(url_for('index', username=current_user.username))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-cancelandrefund/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders_cancel_and_refund(id):
    now = datetime.utcnow()
    item = Vendor_Orders.query.get(id)
    if item:

        msg = db.session\
            .query(Service_ShippingSecret)\
            .filter_by(orderid=id)\
            .first()
        gettracking = db.session\
            .query(Service_Tracking)\
            .filter_by(sale_id=id)\
            .first()

        if item.vendor_id == current_user.id:
            if item.released == 0 and item.cancelled == 0 and item.vendor_id != 0:
                try:
                    p = item.price
                    s = item.shipping_price
                    refund = Decimal(p) + Decimal(s)

                    item.cancelled = 1
                    item.completed = 1
                    item.request_cancel = 0
                    item.completed_time = now
                    item.disputed_order = 0
                    item.waiting_order = 0
                    item.delivered_order = 0
                    item.new_order = 0
                    item.accepted_order = 0

                    db.session.add(item)

                    notification(type=7,
                                 username=item.customer,
                                 user_id=item.customer_id,
                                 salenumber=item.id,
                                 bitcoin=0)

                    btc_cash_sendCointoUser(amount=refund,
                                            comment=item.id,
                                            user_id=item.vendor_id,
                                            )

                    # Give user neg exp
                    exppoint(user=item.customer_id,
                             price=0,
                             type=9,
                             quantity=0,
                             currency=0)
                    if msg:
                        db.session.delete(msg)
                    if gettracking:
                        db.session.delete(gettracking)
                    flash("Order Cancelled", category="danger")
                    db.session.commit()
                    return redirect(url_for('vendor.vendor_orders', username=current_user.username))
                except Exception as e:
                    return redirect(url_for('vendor.vendor_orders', username=current_user.username))
            else:
                flash("Error.  Cancelled already.", category="danger")
                return redirect(url_for('vendor.vendor_orders', username=current_user.username))
        else:
            flash("Vendor id doesnt equal user id", category="danger")
            return redirect(url_for('vendor.vendor_orders', username=current_user.username))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-leavereviewforuser/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def vendor_orders_leave_review_for_user(id):
    now = datetime.utcnow()
    form = vendorleavereview()
    order = Vendor_Orders.query.get(id)
    if order:
        if order.vendor_id == current_user.id:
            userreviews = db.session\
                .query(Profile_Userreviews)\
                .filter(Profile_Userreviews.customer_id == order.customer_id)\
                .order_by(Profile_Userreviews.dateofreview.desc())\
                .limit(20)

            item = db.session\
                .query(Item_MarketItem)\
                .filter(Item_MarketItem.id == order.item_id)\
                .first()

            if request.method == "POST" and form.validate_on_submit():
                if order.cancelled == 0:
                    try:
                        text_box_value_userrating = request.form.get(
                            "item_rating")
                        text_box_value_comment = request.form.get(
                            "reviewcomment")

                        add_feedback = Profile_Userreviews(
                            order_id=order.id,
                            customer=order.customer,
                            customer_id=order.customer_id,
                            review=text_box_value_comment,
                            dateofreview=datetime.utcnow(),
                            rating=text_box_value_userrating,
                        )
                        db.session.add(add_feedback)
                        order.userfeedback = 1

                        db.session.add(order)

                        exppoint(user=order.vendor_id,
                                 price=0,
                                 type=2,
                                 quantity=int(text_box_value_userrating),
                                 currency=0)
                        exppoint(user=order.customer_id,
                                 price=0,
                                 type=6,
                                 quantity=int(text_box_value_userrating),
                                 currency=0)
                        db.session.commit()
                        flash('Feedback submitted.  Exp Points Given..',
                              category='success')
                        return redirect(url_for('vendor.vendor_orders_leave_review_for_user', id=id))

                    except Exception as e:
                        return redirect(url_for('vendor.vendor_orders_leave_review_for_user', id=id))
                else:
                    flash('Cant leave Feedback.  Order was cancelled',
                          category='danger')
                    return redirect(url_for('vendor.vendor_orders_leave_review_for_user', id=id))

            return render_template('/vendor/leavecustomerreview.html',
                                   username=current_user.username,
                                   order=order,
                                   userreviews=userreviews,
                                   item=item,
                                   form=form,
                                   now=now)
        else:
            return redirect(url_for('vendor.Orders'))
    else:
        return redirect(url_for('vendor.Orders'))


@vendor.route('/vendor-deleteorderhistory/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders_delete_order_history(id):

    try:
        item = Vendor_Orders.query.get(id)
        if item.vendor_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            flash("Order Deleted", category="success")
            if item.type == 3:
                return redirect(url_for('vendor.vendoropenTrades', username=current_user.username))
            elif item.type == 2:
                return redirect(url_for('vendor.vendoropenTrades', username=current_user.username))
            else:
                return redirect(url_for('vendor.vendor_orders', username=current_user.username))
        else:
            return redirect(url_for('index', username=current_user.username))
    except:
        flash("Order Deletion error.  Please send feedback/bug", category="danger")
        return redirect(url_for('index', username=current_user.username))


@vendor.route('/vendor-addtracking/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders_add_tracking(id):
    itemcustomer = db.session\
        .query(Vendor_Orders)\
        .filter_by(id=id)\
        .first()
    if itemcustomer.vendor_id == current_user.id:
        tracking = db.session.query(
            Service_Tracking).filter_by(sale_id=id).first()
        if tracking:
            form = addShipping(
                sale_id=itemcustomer.id,
                trackingnumber1=tracking.tracking1,
                selectcarrier1=tracking.carrier1,
                othercarrier1=tracking.othercarrier1,
                trackingnumber2=tracking.tracking2,
                selectcarrier2=tracking.carrier2,
                othercarrier2=tracking.othercarrier2,
                trackingnumber3=tracking.tracking3,
                selectcarrier3=tracking.carrier3,
                othercarrier3=tracking.othercarrier3
            )
            if request.method == 'POST' and form.validate_on_submit():
                car1full = form.selectcarrier1.data
                car1 = car1full.value
                car2full = form.selectcarrier2.data
                car2 = car2full.value
                car3full = form.selectcarrier3.data
                car3 = car3full.value
                if (0 <= car1 <= 4) and (0 <= car2 <= 4) and (0 <= car3 <= 4):
                    tracking.sale_id = itemcustomer.id,
                    tracking.tracking1 = form.trackingnumber1.data,
                    tracking.carrier1 = car1,
                    tracking.othercarrier1 = form.othercarrier1.data,
                    tracking.tracking2 = form.trackingnumber2.data,
                    tracking.carrier2 = car2,
                    tracking.othercarrier2 = form.othercarrier2.data,
                    tracking.tracking3 = form.trackingnumber3.data,
                    tracking.carrier3 = car3,
                    tracking.othercarrier3 = form.othercarrier3.data,

                    db.session.add(tracking)
                    db.session.commit()
                    return redirect(url_for('vendor.vendor_orders', username=current_user.username))

            return render_template('/vendor/addtracking.html', username=current_user.username, form=form)
        else:
            form = addShipping(request.form)
            if request.method == 'POST' and form.validate_on_submit():

                car1full = form.selectcarrier1.data
                car1 = car1full.value

                car2full = form.selectcarrier2.data
                car2 = car2full.value

                car3full = form.selectcarrier3.data
                car3 = car3full.value

                if (0 <= car1 <= 4) and (0 <= car2 <= 4) and (0 <= car3 <= 4):
                    theitem = Service_Tracking(
                        sale_id=itemcustomer.id,
                        tracking1=form.trackingnumber1.data,
                        carrier1=car1,
                        othercarrier1=form.othercarrier1.data,
                        tracking2=form.trackingnumber2.data,
                        carrier2=car2,
                        othercarrier2=form.othercarrier2.data,
                        tracking3=form.trackingnumber3.data,
                        carrier3=car3,
                        othercarrier3=form.othercarrier3.data,
                    )

                    db.session.add(theitem)
                    db.session.commit()

                    return redirect(url_for('vendor.vendor_orders', username=current_user.username))
            return render_template('/vendor/addtracking.html', username=current_user.username, form=form)
    else:
        flash("Cannot view Info.", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-reasonforcancel/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders_reason_for_cancel(id):
    item = db.session.query(Vendor_Orders).filter_by(id=id).first()
    if item.vendor_id == current_user.id:
        return render_template('/vendor/reasontocancel.html', item=item)
    else:
        flash("Cannot view Order.", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-ratings', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_ratings():
    now = datetime.utcnow()
    form = ratingsForm(request.form)
    user, \
        order, \
        issues, \
        getnotifications, \
        customerdisputes \
        = headerfunctions_vendor()

    getavgitem = db.session.query(
        func.avg(User_DataFeedback.item_rating).label("avgitem"))
    getavgitem = getavgitem.filter(User_DataFeedback.vendorid == user.id)
    gitem = getavgitem.all()
    itemscore = str((gitem[0][0]))[:4]

    getavgvendor = db.session.query(
        func.avg(User_DataFeedback.vendorrating).label("avgvendor"))
    getavgvendor = getavgvendor.filter(User_DataFeedback.vendorid == user.id)
    gvendor = getavgvendor.all()
    vendorscore = str((gvendor[0][0]))[:4]

    if vendorscore is None:
        vendorscore = 0
    else:
        vendorscore = vendorscore

    if itemscore is None:
        itemscore = 0
    else:
        itemscore = itemscore

    # Pagination
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()
    # PEr Page tells how many search results pages
    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 25
    # end pagination

    ratings = db.session\
        .query(User_DataFeedback)\
        .filter_by(vendorid=current_user.id)\
        .order_by(User_DataFeedback.timestamp.desc())
    ratings = ratings.limit(per_page).offset(offset)

    pagination = Pagination(page=page,
                            total=ratings.count(),
                            search=search,
                            record_name='ratings',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap5',
                            inner_window=inner_window,
                            outer_window=outer_window)

    if request.method == 'POST':
        ratingdata = form.sortrating.data

        if ratingdata == '0':
            pass
        elif ratingdata == '1':
            # Newest ratings first
            r = db.session.query(User_DataFeedback)
            r = r.filter_by(vendorid=user.id)
            r = r.order_by(User_DataFeedback.timestamp.desc())
            ratings = r.limit(per_page).offset(offset)

        elif ratingdata == '2':
            # Highest vendor ratings first
            r = db.session.query(User_DataFeedback)
            r = r.filter_by(vendorid=user.id)
            r = r.order_by(User_DataFeedback.vendorrating.desc())
            ratings = r.limit(per_page).offset(offset)

        elif ratingdata == '3':
            # Highest vendor ratings first
            r = db.session.query(User_DataFeedback)
            r = r.filter_by(vendorid=user.id)
            r = r.order_by(User_DataFeedback.vendorrating.asc())
            ratings = r.limit(per_page).offset(offset)
        else:
            flash("Invalid Selection.", category="danger")
            return redirect(url_for('index'))

    return render_template('/vendor/vendorRatings.html',
                           user=user, now=now,
                           form=form,
                           ratings=ratings,
                           itemscore=itemscore,
                           vendorscore=vendorscore,
                           pagination=pagination,
                           order=order,
                           issues=issues,
                           getnotifications=getnotifications,
                           customerdisputes=customerdisputes
                           )


@vendor.route('/vendor-viewfeedbackspecific/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def vendor_feddback_view_specific(id):
    try:
        now = datetime.utcnow()
        form = feedbackcomment(request.form)

        user = db.session\
            .query(Auth_User)\
            .filter_by(username=current_user.username)\
            .first()
        rating = db.session\
            .query(User_DataFeedback)\
            .filter_by(id=id)\
            .first()
        ileftfeedback = db.session\
            .query(Profile_FeedbackComments)\
            .filter_by(feedback_id=id)\
            .first()
        order = db.session\
            .query(Vendor_Orders)\
            .filter_by(id=rating.sale_id)\
            .first()
        if order is not None:
            if order.vendor_id == current_user.id:
                return render_template('/vendor/viewspecificfeedback.html',
                                       user=user, now=now,
                                       ileftfeedback=ileftfeedback,
                                       rating=rating,
                                       form=form,
                                       order=order)
            else:
                flash("Cannot view Order.", category="danger")
                return redirect(url_for('index'))
        else:
            flash("Order doesnt exist.", category="danger")
            return redirect(url_for('index'))

    except Exception as e:
        flash("Feedback on order error.", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor_orders_view_specific/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def vendor_orders_view_specific(id):
    order = db.session.query(Vendor_Orders).filter_by(id=id).first()
    if order:
        if order.customer_id == current_user.id or order.vendor_id == current_user.id or current_user.admin_role <= 3:
            if current_user.id == order.vendor_id and order.request_return == 1:
                return redirect(url_for('vendor.vendor_add_temp_address', id=id))

            if current_user.id == order.customer_id and order.request_return == 2:
                return redirect(url_for('auth.orders_customer_return_instructions', id=id))
            else:

                tracking = db.session\
                    .query(Service_Tracking)\
                    .filter_by(sale_id=id)\
                    .first()
                getitem = db.session\
                    .query(Item_MarketItem)\
                    .filter(Item_MarketItem.id == order.item_id)\
                    .first()
                # delete return address
                returninfo = db.session\
                    .query(Service_Returns)\
                    .filter_by(ordernumber=id)\
                    .first()
                returns = db.session\
                    .query(Service_Returns)\
                    .filter_by(ordernumber=order.id)\
                    .first()
                # delete return tracking
                returntracking = db.session\
                    .query(Service_ReturnsTracking)\
                    .filter_by(ordernumber=id)\
                    .first()
                vendortracking = db.session\
                    .query(Service_Tracking)\
                    .filter_by(sale_id=id)\
                    .first()

                # get the message and tracking for order
                msg = db.session\
                    .query(Service_ShippingSecret)\
                    .filter_by(orderid=id)\
                    .first()
                gettracking = db.session\
                    .query(Service_Tracking)\
                    .filter_by(sale_id=id)\
                    .first()
                if msg:
                    msg = msg
                else:
                    msg = 2
                return render_template('/vendor/vendor_orders_view_specific.html',
                                       order=order,
                                       item=getitem,
                                       returninfo=returninfo,
                                       returntracking=returntracking,
                                       returns=returns,
                                       vendortracking=vendortracking,
                                       msg=msg,
                                       gettracking=gettracking,
                                       tracking=tracking
                                       )
        else:
            flash("Cannot view Order.", category="danger")
            return redirect(url_for('index'))
    else:
        flash("Order doesnt exist on clearnet_webapp.", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-refunds', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_refunds():
    now = datetime.utcnow()

    user, \
        order, \
        issues, \
        getnotifications, \
        customerdisputes \
        = headerfunctions_vendor()

    # See if user has default return address
    try:
        getdefaultreturn = db.session\
            .query(Service_DefaultReturns)\
            .filter_by(username=user.username)\
            .first()
        if getdefaultreturn:
            getdefaultreturn = 1
        else:
            getdefaultreturn = 0
    except Exception:
        getdefaultreturn = 0

    disputed = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.vendor == current_user.username, Vendor_Orders.disputed_order == 1)\
        .all()

    returnorder = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.vendor == current_user.username, Vendor_Orders.request_return.between(1, 3))\
        .all()

    return render_template('/vendor/vendor_refunds.html',
                           returnorder=returnorder,
                           getdefaultreturn=getdefaultreturn,
                           disputed=disputed,
                           now=now,
                           user=user,
                           order=order,
                           issues=issues,
                           getnotifications=getnotifications,
                           customerdisputes=customerdisputes
                           )


@vendor.route('/return-add-address/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_add_temp_address(id):
    now = datetime.utcnow()
    form = addtempreturn()
    order = db.session\
        .query(Vendor_Orders)\
        .filter_by(id=id)\
        .first()

    # figure out price
    getitem = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.id == order.item_id)\
        .first()
    totalprice = (Decimal(order.shipping_price) + Decimal(order.price))

    msg = db.session\
        .query(Service_ShippingSecret)\
        .filter_by(orderid=id)\
        .first()
    gettracking = db.session\
        .query(Service_Tracking)\
        .filter_by(sale_id=id)\
        .first()
    if request.method == 'POST' and form.validate_on_submit():
        if current_user.id == order.vendor_id:
            if order.released == 0 and order.completed == 0:
                if form.submit.data:
                    addtemp = Service_Returns(
                        ordernumber=id,
                        name=form.name.data,
                        street=form.street.data,
                        city=form.city.data,
                        state=form.state.data,
                        country=form.country.data,
                        zip=form.zip.data,
                        message=form.messagereturn.data,
                    )
                    db.session.add(addtemp)
                    db.session.flush()

                    order.return_id = addtemp.id
                    order.request_return = 2
                    db.session.add(order)

                    db.session.commit()
                    flash("Return address added for Order#" + str(order.id),
                          category="success")
                    return redirect(url_for('vendor.vendor_refunds', username=current_user.username))

                elif form.cancelandrefund.data:

                    order.completed = 1
                    order.disputed_order = 0
                    order.new_order = 0
                    order.accepted_order = 0
                    order.waiting_order = 0
                    order.delivered_order = 1
                    order.request_cancel = 0
                    order.reason_cancel = 0
                    order.request_return = 0
                    order.released = 1
                    order.cancelled = 0
                    order.incart = 0
                    order.modid = 0
                    order.completed_time = now

                    db.session.add(order)

                    notification(type=111,
                                 username=order.customer,
                                 user_id=order.customer_id,
                                 salenumber=order.id,
                                 bitcoin=0)
                    notification(type=111, username=order.vendor,
                                 user_id=order.vendor_id,
                                 salenumber=order.id,
                                 bitcoin=0)

                    btc_cash_sendCointoclearnet(amount=order.fee,
                                                comment=order.id,
                                                shard=current_user.shard
                                                )
                    btc_cash_sendCointoUser(amount=totalprice,
                                            comment=order.id,
                                            user_id=order.vendor_id,
                                            )

                    # BTC CASH Spent by user
                    userdata_total_spent_on_item_bch(
                        user_id=order.customer_id, howmany=1, amount=order.price)

                    # BTC CASH recieved by vendor
                    userdata_total_made_on_item_bch(
                        user_id=order.vendor_id, amount=order.price)

                    # Delete temp message vendor gave
                    if msg:
                        db.session.delete(msg)
                    if gettracking:
                        db.session.delete(gettracking)

                    # Add total items bought
                    userdata_add_total_items_bought(
                        user_id=order.customer_id, howmany=order.quantity)

                    # add total sold to vendor
                    addtotalItemsSold(user_id=order.vendor_id,
                                      howmany=order.quantity)

                    # add diff trading partners
                    userdata_different_trading_partners_user(
                        user_id=order.customer_id, otherid=order.vendor_id)
                    userdata_different_trading_partners_vendor(
                        user_id=order.vendor_id, otherid=order.customer_id)

                    # customer exp for finishing early
                    exppoint(user=order.customer_id, price=0,
                             type=5, quantity=0, currency=0)

                    # Give Vendor experience points for sale
                    exppoint(user=order.vendor_id, price=order.price, type=10,
                             quantity=order.quantity, currency=order.currency)

                    # Give user experience points for sale
                    exppoint(user=order.customer_id, price=order.price, type=1,
                             quantity=order.quantity, currency=order.currency)

                    db.session.commit()
                    flash(f"Cancelled and refunded. Order# {order.id}", category="success")
                    return redirect(url_for('vendor.vendor_refunds', username=current_user.username))
                else:
                    flash("Error", category="danger")
                    return redirect(url_for('index', username=current_user.username))
            else:
                flash("Error", category="danger")
                return redirect(url_for('index', username=current_user.username))
        else:
            flash("Error", category="danger")
            return redirect(url_for('index', username=current_user.username))
    return render_template('/vendor/vendor_orders_view_specific.html',
                           form=form,
                           order=order,
                           msg=msg,
                           gettracking=gettracking,
                           item=getitem,
                           )


@vendor.route('/return-edit-address/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_edit_temp_address(id):
    returnaddress = db.session\
        .query(Service_Returns)\
        .filter_by(ordernumber=id)\
        .first()
    order = db.session\
        .query(Vendor_Orders)\
        .filter_by(id=id)\
        .first()
    getitem = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.id == order.item_id)\
        .first()
    # vendor is True

    try:
        form = addtempreturn(
            ordernumber=returnaddress.id,
            name=returnaddress.name,
            street=returnaddress.street,
            city=returnaddress.city,
            state=returnaddress.state,
            country=returnaddress.country,
            zip=returnaddress.zip,
            messagereturn=returnaddress.message
        )
    except Exception:
        form = addtempreturn()

    if request.method == 'POST' and form.validate_on_submit():
        returnaddress.ordernumber = id,
        returnaddress.name = form.name.data,
        returnaddress.street = form.street.data,
        returnaddress.city = form.city.data,
        returnaddress.state = form.state.data,
        returnaddress.country = form.country.data,
        returnaddress.zip = form.zip.data,
        returnaddress.message = form.messagereturn.data,

        db.session.add(returnaddress)
        db.session.commit()
        flash(f"Return address added for Order# {order.id}", category="success")
        return redirect(url_for('vendor.vendor_refunds', username=current_user.username))

    return render_template('/vendor/vendor_orders_view_specific.html',  form=form,
                           order=order,
                           vendor=vendor,
                           item=getitem,
                           returnaddress=returnaddress,
                           )


@vendor.route('/vendor-markasreturned/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendor_returns_orders_recieve(id):
    now = datetime.utcnow()
    # sent vendor order to recieved
    vendororder = db.session\
        .query(Vendor_Orders)\
        .filter_by(id=id)\
        .first()
    msg = db.session\
        .query(Service_ShippingSecret)\
        .filter_by(orderid=id)\
        .first()
    gettracking = db.session\
        .query(Service_Tracking)\
        .filter_by(sale_id=id)\
        .first()

    if vendororder.vendor_id == current_user.id and vendororder.released == 0:
        vendororder.request_return = 5
        vendororder.completed = 1
        vendororder.new_order = 0
        vendororder.released = 1
        vendororder.accepted_order = 0
        vendororder.waiting_order = 0
        vendororder.delivered_order = 0
        vendororder.completed_time = now

        db.session.add(vendororder)

        try:
            # Delete temp message vendor gave
            tempaddress = db.session\
                .query(Service_Returns)\
                .filter_by(ordernumber=id)\
                .first()
            if tempaddress:
                db.session.delete(tempaddress)

            # Delete temp message vendor gave
            if msg:
                db.session.delete(msg)
            if gettracking:
                db.session.delete(gettracking)
        except:
            db.session.rollback()

        try:
            # delete return tracking number
            returntracking = db.session\
                .query(Service_ReturnsTracking)\
                .filter_by(ordernumber=id)\
                .first()
            db.session.delete(returntracking)

        except:
            db.session.rollback()
        # give user bad exp

        exppoint(user=vendororder.customer_id, price=0,
                 type=10, quantity=0, currency=0)

        # calculate vendor amount
        pricewithoutshipping = Decimal(vendororder.price)
        shiprice = Decimal(vendororder.shipping_price)
        refundamount = Decimal(vendororder.return_amount)

        # he gets shipping + cost leftover after quant
        vendorgets = (pricewithoutshipping-refundamount) + shiprice
        comment = str(vendororder.id)

        # notify customer
        notification(type=8,
                     username=vendororder.customer,
                     user_id=vendororder.customer_id,
                     salenumber=vendororder.id,
                     bitcoin=vendororder.return_amount)
        # transfer money back to user from clearnet account
        # notify vendor
        notification(type=6,
                     username=vendororder.customer,
                     user_id=vendororder.customer_id,
                     salenumber=vendororder.id,
                     bitcoin=vendororder.return_amount
                     )
        # notify vendor
        notification(type=8,
                     username=vendororder.vendor,
                     user_id=vendororder.vendor_id,
                     salenumber=vendororder.id,
                     bitcoin=0
                     )

        btc_cash_sendCointoUser(amount=vendororder.return_amount,
                                comment=comment,
                                user_id=vendororder.vendor_id,
                                )

        if vendorgets > 0:

            btc_cash_sendCointoUser(amount=vendorgets,
                                    comment=comment,
                                    user_id=vendororder.vendor_id,
                                    )

        try:
            # delete return address
            returninfo = db.session\
                .query(Service_Returns)\
                .filter_by(ordernumber=id)\
                .first()
            if returninfo:
                db.session.delete(returninfo)
        except Exception:
            pass
        try:
            # delete return tracking
            returntracking = db.session\
                .query(Service_ReturnsTracking)\
                .filter_by(ordernumber=id)\
                .first()
            if returntracking:
                db.session.delete(returntracking)
        except Exception:
            pass
        db.session.commit()
        flash("Order Marked as returned", category="success")
        return redirect(url_for('vendor.vendor_orders', username=current_user.username))
    else:
        return redirect(url_for('index'))


@vendor.route('/vendor-orders', methods=['GET'])
@website_offline
@login_required
@vendoraccount_required
def vendor_orders():
    now = datetime.utcnow()
    user, \
        order, \
        issues, \
        getnotifications, \
        customerdisputes \
        = headerfunctions_vendor()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()
    # PEr Page tells how many search results pages
    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 10

    ordernew_overall = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.vendor_id == user.id,
                Vendor_Orders.new_order == 1,
                Vendor_Orders.completed == 0,
                Vendor_Orders.type == 1
                )\
        .order_by(Vendor_Orders.id.desc())
    ordernew = ordernew_overall.limit(per_page).offset(offset)
    ordernewcount = ordernew_overall.count()
    paginationordernew = Pagination(page=page,
                                    total=ordernew_overall.count(),
                                    search=search,
                                    record_name='items',
                                    offset=offset,
                                    per_page=per_page,
                                    css_framework='bootstrap5',
                                    inner_window=inner_window,
                                    outer_window=outer_window)

    orderaccepted1 = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.vendor_id == user.id,
                Vendor_Orders.accepted_order == 1,
                Vendor_Orders.completed == 0,
                Vendor_Orders.type == 1
                )

    orderaccepted1 = orderaccepted1.order_by(Vendor_Orders.id.desc())
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

    orderwaiting1 = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.vendor_id == user.id,
                Vendor_Orders.waiting_order == 1,
                Vendor_Orders.completed == 0,
                Vendor_Orders.type == 1
                )
    orderwaiting1 = orderwaiting1.order_by(Vendor_Orders.id.desc())
    orderwaiting = orderwaiting1.limit(per_page).offset(offset)
    orderwaitingcount = orderwaiting1.count()
    paginationorderwaiting = Pagination(page=page,
                                        total=orderwaiting1.count(),
                                        search=search,
                                        record_name='items',
                                        offset=offset,
                                        per_page=per_page,
                                        css_framework='bootstrap5',
                                        inner_window=inner_window,
                                        outer_window=outer_window)

    completed1 = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.vendor_id == user.id,
                Vendor_Orders.completed == 1,
                Vendor_Orders.type == 1
                )
    completed1 = completed1.order_by(Vendor_Orders.id.desc())
    completed = completed1.limit(per_page).offset(offset)
    completedcount = completed1.count()
    paginationcompleted = Pagination(page=page,
                                     total=completed1.count(),
                                     search=search,
                                     record_name='items',
                                     offset=offset,
                                     per_page=per_page,
                                     css_framework='bootstrap5',
                                     inner_window=inner_window,
                                     outer_window=outer_window)

    return render_template('/vendor/vendor_orders.html',
                           user=user, now=now,
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
                           order=order,
                           issues=issues,
                           getnotifications=getnotifications,
                           customerdisputes=customerdisputes
                           )
