from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.orders import orders
from app import db, UPLOADED_FILES_DEST

from flask_paginate import Pagination, get_page_args
from datetime import datetime
from decimal import Decimal

from app.exppoints import exppoint
from app.notification import notification
from app.search.searchfunction import headerfunctions
from app.userdata.views import \
    userdata_add_total_items_bought, \
    addtotalItemsSold, \
    userdata_different_trading_partners_user, \
    userdata_different_trading_partners_vendor, \
    userdata_total_made_on_item_bch, \
    userdata_total_spent_on_item_bch, \
    userdata_reviews_given, \
    userdata_reviews_recieved, \
    userdata_aff_stats

# btc cash work
from app.wallet_bch.wallet_btccash_work import \
    btc_cash_sendCointoclearnet, \
    btc_cash_sendcointoaffiliate, \
    btc_cash_sendCointoUser
from app.common.decorators import \
    ping_user, \
    website_offline, \
    login_required

# forms
from app.auth.forms import searchForm
from app.auth.forms import \
    feedbackonorderForm, \
    requestCancelform, \
    returnitem_form_factory, \
    markasSent

# models
from app.classes.auth import \
    Auth_User
from app.classes.affiliate import \
    Affiliate_Overview
from app.classes.item import \
    Item_MarketItem
from app.classes.service import \
    Service_ShippingSecret, \
    Service_Returns, \
    Service_ReturnsTracking, \
    Service_Tracking
from app.classes.category import Category_Categories
from app.classes.userdata import \
    User_DataFeedback
from app.classes.vendor import \
    Vendor_Orders
from app.classes.wallet_bch import Bch_Prices


@orders.route('/orders', methods=['GET', 'POST'])
@website_offline
@login_required
def orders_home():
    user, \
        order, \
        tot, \
        issues, \
        getnotifications, \
        allmsgcount, \
        userbalance, \
        unconfirmed, \
        customerdisputes = headerfunctions()
    feedbackform = feedbackonorderForm(request.form)
    formsearch = searchForm()

    get_cats = db.session\
        .query(Category_Categories)\
        .filter(Category_Categories.id != 1000, Category_Categories.id != 0)\
        .order_by(Category_Categories.name.asc())\
        .all()
    # forms

    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()

    # PEr Page tells how many search results pages
    per_page = 10
    inner_window = 1  # search bar at bottom used for .. lots of pages
    outer_window = 1  # search bar at bottom used for .. lots of pages

    user = db.session.query(Auth_User).filter_by(
        username=current_user.username).first()

    btc_cash_price = db.session.query(Bch_Prices).all()

    myorders = db.session.query(Vendor_Orders)
    myorders = myorders.filter((Vendor_Orders.customer_id == current_user.id))
    myorders = myorders.filter(Vendor_Orders.vendor_id != 0)
    myorders = myorders.order_by(Vendor_Orders.age.desc())
    orders = myorders.limit(per_page).offset(offset)
    myorderscount = myorders.count()

    # get return by
    now = datetime.utcnow()

    pagination = Pagination(page=page,
                            now=now,
                            total=myorders.count(),
                            search=search,
                            record_name='items',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap4',
                            inner_window=inner_window,
                            outer_window=outer_window)

    if request.method == 'POST':
        if formsearch.validate_on_submit():
            # cats
            categoryfull = formsearch.category.data
            cat = categoryfull.id

            # catch dynamic variables
            if formsearch.searchString.data == '' and cat == 0:
                return redirect(url_for('index'))

            if formsearch.searchString.data == '':
                formsearch.searchString.data = cat

            return redirect(url_for('search.search_master',
                                    searchterm=formsearch.searchString.data,
                                    function=cat,

                                    ))

        if feedbackform.submitfeedback.data:
            if feedbackform.validate_on_submit():

                my_id = request.form.get("my_id", "")
                getitemid = db.session.query(
                    Vendor_Orders).filter_by(id=my_id).first()

                if getitemid.customer_id == current_user.id:
                    if getitemid.feedback == 0:
                        if getitemid.type == 3:
                            text_box_value_vendorrating = request.form.get(
                                "vendorrating")
                            text_box_value_item_rating = 0
                        else:
                            text_box_value_vendorrating = request.form.get(
                                "vendorrating")
                            text_box_value_item_rating = request.form.get(
                                "item_rating")
                        if text_box_value_vendorrating and text_box_value_item_rating is not None:
                            if (1 <= int(text_box_value_vendorrating) <= 5) \
                                    and (1 <= int(text_box_value_item_rating) <= 5):
                                add = User_DataFeedback(
                                    type=getitemid.type,
                                    sale_id=getitemid.id,
                                    timestamp=now,
                                    vendorname=getitemid.vendor,
                                    vendorid=getitemid.vendor_id,
                                    customername=current_user.username,
                                    author_id=current_user.id,
                                    comment=feedbackform.feedbacktext.data,
                                    item_rating=text_box_value_item_rating,
                                    vendorrating=text_box_value_vendorrating,
                                    item_id=getitemid.item_id,
                                    addedtodb=0,
                                )
                                getitemid.feedback = 1

                                db.session.add(add)
                                db.session.add(getitemid)

                                # add a review
                                userdata_reviews_given(user_id=user.id)
                                userdata_reviews_recieved(
                                    user_id=getitemid.vendor_id)

                                # vendorexp based off score results
                                exppoint(user=getitemid.vendor_id,
                                         price=0,
                                         type=7,
                                         quantity=int(text_box_value_vendorrating), currency=0)

                                # customer exp for giving review based off score results
                                exppoint(user=current_user.id,
                                         price=0,
                                         type=3,
                                         quantity=int(
                                             text_box_value_vendorrating),
                                         currency=0)

                                db.session.commit()

                                flash('Feedback submitted. '
                                      ' Exp Points Given for the feedback!.', 'success')
                                return redirect(url_for('orders.orders_home'))
                            else:
                                flash('Invalid Review. '
                                      'Please make sure you filled out the ratings and feedback. '
                                      'Must be Longer than 10 characters)',
                                      category="danger")
                                return redirect(url_for('orders.orders_home'))

                        else:
                            flash('Invalid Review. '
                                  'Please make sure you filled out the ratings and feedback. '
                                  'Must be longer than 10 characters)',
                                  category="danger")
                            return redirect(url_for('orders.orders_home'))
                    else:
                        flash('Item already reviewed',
                              category="danger")
                        return redirect(url_for('orders.orders_home'))
                else:
                    flash('Invalid User.',
                          category="danger")
                    return redirect(url_for('orders.orders_home'))
            else:
                flash('Invalid Review.'
                      'Please make sure you filled out the ratings and feedback. longer than 10 characters',
                      category="danger")
                return redirect(url_for('orders.orders_home'))

    return render_template('/auth/orders/orders.html',
                           form=formsearch,
                           # header stuff
                           btc_cash_price=btc_cash_price,
                           get_cats=get_cats,
                           order=order,
                           tot=tot,
                           issues=issues,
                           getnotifications=getnotifications,
                           allmsgcount=allmsgcount,
                           userbalance=userbalance,
                           customerdisputes=customerdisputes,
                           unconfirmed=unconfirmed,
                           user=user, now=now,
                           feedbackform=feedbackform,
                           myorders=myorders,
                           myorderscount=myorderscount,
                           pagination=pagination,
                           orders=orders
                           )


@orders.route('/order-tracking/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def orders_view_tracking(id):
    now = datetime.utcnow()
    form = searchForm()
    user = db.session\
        .query(Auth_User)\
        .filter_by(username=current_user.username)\
        .first()
    order = db.session\
        .query(Vendor_Orders)\
        .filter_by(id=id)\
        .first()
    if order:
        msg = db.session\
            .query(Service_ShippingSecret)\
            .filter_by(orderid=id)\
            .first()
        tracking = db.session\
            .query(Service_Tracking)\
            .filter_by(sale_id=id)\
            .first()

        if order.customer_id == current_user.id:
            return render_template('/auth/orders/tracking.html',
                                   order=order,
                                   user=user,
                                   now=now,
                                   tracking=tracking,
                                   form=form,
                                   msg=msg)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@orders.route('/order-customerservice', methods=['GET', 'POST'])
@website_offline
@login_required
def orders_customer_service():
    return redirect(url_for('auth.setup_account'))


@orders.route('/customer-returninstructions/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def orders_customer_return_instructions(id):
    now = datetime.utcnow()
    trackingform = markasSent(request.form)

    order = db.session\
        .query(Vendor_Orders)\
        .filter_by(id=id)\
        .first()
    if order:
        if order.customer_id == current_user.id or order.vendor_id == current_user.id:
            # item
            getitem = db.session\
                .query(Item_MarketItem)\
                .filter(Item_MarketItem.id == order.item_id)\
                .first()
            vendortracking = db.session\
                .query(Service_Tracking)\
                .filter_by(sale_id=id)\
                .first()
            # delete return address
            returninfo = db.session\
                .query(Service_Returns)\
                .filter_by(ordernumber=id)\
                .first()
            # delete return tracking
            returntracking = db.session\
                .query(Service_ReturnsTracking)\
                .filter_by(ordernumber=id)\
                .first()
            # customer tracking address
            msg = db.session\
                .query(Service_ShippingSecret)\
                .filter_by(orderid=id)\
                .first()
            gettracking = db.session\
                .query(Service_Tracking)\
                .filter_by(sale_id=id)\
                .first()
            # Customer Return address check if added
            # if 0 no address added
            # if 1 address added

            returns = db.session\
                .query(Service_Returns)\
                .filter_by(ordernumber=order.id)\
                .first()
            returnscount = db.session\
                .query(Service_Returns)\
                .filter_by(ordernumber=order.id)\
                .count()
            # get default address or a temporary one
            # if 0 no address at all either default or temp
            # Customer Return tracking ..initated return and 14 days
            if request.method == 'POST':
                if trackingform.validate_on_submit():
                    try:
                        car1full = trackingform.carrier.data
                        car1 = car1full.value
                        addnewreturn = Service_ReturnsTracking(
                            ordernumber=order.id,
                            timestamp=now,
                            customername=order.customer,
                            customerid=order.customer_id,
                            vendorname=order.vendor,
                            vendorid=getitem.vendor_id,
                            carrier=car1,
                            trackingnumber=trackingform.trackingnumber.data,
                            othercarrier=trackingform.othercarrier.data,
                        )

                        order.request_return = 3
                        order.returncancelage = datetime.utcnow()

                        db.session.add(order)
                        db.session.add(addnewreturn)
                        notification(type=555,
                                     username=order.vendor,
                                     user_id=order.vendor_id,
                                     salenumber=order.id,
                                     bitcoin=0)

                        db.session.commit()
                        return redirect(url_for('auth.orders_customer_return_instructions', id=id))
                    except Exception as e:
                        flash(str(e), 'danger')
                        flash('Invalid Submit.', 'danger')
                        return redirect(url_for('auth.orders_customer_return_instructions', id=id))

                return redirect(url_for('auth.orders_customer_return_instructions', id=id))

            return render_template('/vendor/vendor_orders_view_specific.html',
                                   order=order,
                                   item=getitem,
                                   returns=returns,
                                   returninfo=returninfo,
                                   returntracking=returntracking,
                                   returnscount=returnscount,
                                   trackingform=trackingform,
                                   vendortracking=vendortracking,
                                   msg=msg,
                                   gettracking=gettracking
                                   )
    else:
        return redirect(url_for('index'))


@orders.route('/order-cancel/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def orders_cancel_order(id):
    now = datetime.utcnow()
    try:
        getorder = db.session.query(Vendor_Orders).filter_by(id=id).first()
        if getorder:
            msg = db.session.query(
                Service_ShippingSecret).filter_by(orderid=id).first()
            gettracking = db.session.query(
                Service_Tracking).filter_by(sale_id=id).first()
            totalprice = (Decimal(getorder.shipping_price) +
                          Decimal(getorder.price))
            if getorder.customer_id == current_user.id or getorder.vendor_id == current_user.id:
                if getorder.released == 0 \
                        and getorder.waiting_order == 0 \
                        and getorder.disputed_order == 0 \
                        and getorder.cancelled == 0 \
                        and getorder.accepted_order == 0 \
                        and getorder.delivered_order == 0 \
                        and getorder.vendor_id != 0:

                    getorder.disputed_order = 0
                    getorder.new_order = 0
                    getorder.accepted_order = 0
                    getorder.waiting_order = 0
                    getorder.delivered_order = 1
                    getorder.request_cancel = 0
                    getorder.reason_cancel = 0
                    getorder.request_return = 0
                    getorder.cancelled = 1
                    getorder.incart = 0
                    getorder.modid = 0
                    getorder.released = 1
                    getorder.completed = 1
                    getorder.completed_time = now

                    db.session.add(getorder)

                    btc_cash_sendCointoUser(amount=totalprice,
                                            comment=getorder.id,
                                            user_id=getorder.customer_id,
                                            )

                    if gettracking:
                        db.session.delete(gettracking)

                    if msg:
                        db.session.delete(msg)

                    if getorder.type == 1:
                        getitem = db.session.query(Item_MarketItem).filter(
                            getorder.item_id == Item_MarketItem.id).first()
                        x = getitem.item_count
                        y = getorder.quantity
                        z = x + y
                        getitem.item_count = z

                        db.session.add(getitem)

                    # Give user neg exp
                    flash("Order #" + str(id) +
                          " Cancelled.  Shipping info deleted", category="success")
                    exppoint(user=getorder.customer_id,
                             price=0,
                             type=8,
                             quantity=0,
                             currency=0)
                    notification(type=7,
                                 username=getorder.customer,
                                 user_id=getorder.customer_id,
                                 salenumber=getorder.id,
                                 bitcoin=0)
                    notification(type=7,
                                 username=getorder.vendor,
                                 user_id=getorder.vendor_id,
                                 salenumber=getorder.id,
                                 bitcoin=0)
                    db.session.commit()
                    return redirect(url_for('orders.orders_home'))
                else:
                    flash("Order #" + str(id) +
                          " cannot be processed with request", category="danger")
                    return redirect(url_for('orders.orders_home'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    except:
        return redirect(url_for('orders.orders_home'))


@orders.route('/order-recieved/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def orders_mark_as_recieved(id):

    now = datetime.utcnow()
    try:
        getorder = db.session.query(Vendor_Orders).filter_by(id=id).first()
        physicalitemfee = getorder.fee
        if getorder:
            if getorder.customer_id == current_user.id:
                if getorder.completed == 0 and getorder.released == 0 and getorder.vendor_id != 0:
                    if getorder.waiting_order == 1 or getorder.accepted_order == 1:

                        shiprice = (Decimal(getorder.shipping_price) +
                                    Decimal(getorder.price) - getorder.fee)
                        msg = db.session.query(Service_ShippingSecret).filter_by(
                            orderid=getorder.id).first()
                        gettracking = db.session.query(Service_Tracking).filter_by(
                            sale_id=getorder.id).first()

                        getorder.completed = 1
                        getorder.disputed_order = 0
                        getorder.new_order = 0
                        getorder.accepted_order = 0
                        getorder.waiting_order = 0
                        getorder.delivered_order = 1
                        getorder.request_cancel = 0
                        getorder.reason_cancel = 0
                        getorder.request_return = 0
                        getorder.released = 1
                        getorder.cancelled = 0
                        getorder.incart = 0
                        getorder.modid = 0
                        getorder.completed_time = now

                        db.session.add(getorder)

                        notification(type=111,
                                     username=getorder.customer,
                                     user_id=getorder.customer_id,
                                     salenumber=getorder.id,
                                     bitcoin=0
                                     )
                        notification(type=111,
                                     username=getorder.vendor,
                                     user_id=getorder.vendor_id,
                                     salenumber=getorder.id,
                                     bitcoin=0
                                     )

                        # split the profit and how much affiliate gets
                        if getorder.affiliate_code != 0 and getorder.affiliate_discount_percent != 0:
                            getpromo = db.session\
                                .query(Affiliate_Overview) \
                                .filter(Affiliate_Overview.promocode == getorder.affiliate_code)\
                                .first()

                            # variables
                            promopercent = (Decimal(getpromo.aff_fee / 100))

                            amounttomodify = (
                                Decimal(getorder.price_beforediscount))

                            # percent for affiliate
                            # multiply amount before fee off *  promo percent
                            amount_to_affiliate = (
                                amounttomodify * promopercent)

                            # percent to protos
                            # physicalfeefor item - feeforaffiliate == feeforprotos
                            feeforprotos = physicalitemfee - promopercent

                            #  amounttomnodify * feeforprotos
                            amount_to_protos = amounttomodify * feeforprotos

                            # fee for affiliate
                            getorder.affiliate_profit = amount_to_affiliate
                            db.session.add(getorder)

                            # order the amount sent
                            btc_cash_sendcointoaffiliate(amount=amount_to_affiliate,
                                                         comment=getorder.id,
                                                         user_id=getpromo.user_id
                                                         )

                            btc_cash_sendCointoclearnet(amount=amount_to_protos,
                                                        comment=getorder.id,
                                                        shard=current_user.shard
                                                        )
                            # add affiliate stats
                            userdata_aff_stats(user_id=getpromo.user_id,
                                               amount=amount_to_affiliate, currency=3)

                            # send amount to user
                            btc_cash_sendCointoUser(amount=shiprice,
                                                    comment=getorder.id,
                                                    user_id=getorder.vendor_id,
                                                    )
                            db.session.flush()
                        # delete shipping
                        if msg is not None:
                            print("deleting message")
                            print(msg.id)
                            db.session.delete(msg)

                        if gettracking:
                            db.session.delete(gettracking)

                        # STATS
                        # BTC CASH Spent by user
                        userdata_total_spent_on_item_bch(user_id=getorder.customer_id,
                                                         howmany=1,
                                                         amount=getorder.price
                                                         )

                        # BTC CASH recieved by vendor
                        userdata_total_made_on_item_bch(user_id=getorder.vendor_id,
                                                        amount=shiprice
                                                        )

                        # Add total items bought
                        userdata_add_total_items_bought(
                            user_id=getorder.customer_id, howmany=getorder.quantity)

                        # add total sold to vendor
                        addtotalItemsSold(
                            user_id=getorder.vendor_id, howmany=getorder.quantity)

                        # add diff trading partners
                        userdata_different_trading_partners_user(
                            user_id=getorder.customer_id, otherid=getorder.vendor_id)

                        userdata_different_trading_partners_vendor(
                            user_id=getorder.vendor_id, otherid=getorder.customer_id)

                        # customer exp for finishing early
                        exppoint(user=getorder.customer_id, price=0,
                                 type=5, quantity=0, currency=0)

                        # Give Vendor experience points for sale
                        exppoint(user=getorder.vendor_id,
                                 price=getorder.price,
                                 type=11,
                                 quantity=getorder.quantity,
                                 currency=getorder.currency)

                        # Give user experience points for sale
                        exppoint(user=getorder.customer_id,
                                 price=getorder.price,
                                 type=1,
                                 quantity=getorder.quantity,
                                 currency=getorder.currency)

                        db.session.commit()

                        flash("Order #" + str(id) + " recieved. "
                                                    "Exp rewarded for finalizing Early."
                                                    " Shipping info deleted", category="success")
                        return redirect(url_for('orders.orders_home'))
                    else:
                        flash("Order #" + str(id) +
                              ": Cannot Finalize", category="success")
                        return redirect(url_for('orders.orders_home'))
                else:
                    flash("Order #" + str(id) +
                          " already completed", category="success")
                    return redirect(url_for('orders.orders_home'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    except Exception as e:
        print(str(e))
        return redirect(url_for('orders.orders_home'))


@orders.route('/order-requestcancel/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def orders_request_cancel_order(id):
    cancelorder = db.session.query(Vendor_Orders).filter_by(id=id).first()
    if cancelorder:
        if cancelorder.accepted_order == 1 \
                and cancelorder.completed == 0 \
                and cancelorder.vendor_id != 0 \
                and cancelorder.released == 0:
            try:
                form = requestCancelform(request.form)
                cancelorder = db.session.query(
                    Vendor_Orders).filter_by(id=id).first()
                if request.method == 'POST':
                    x = form.type.data
                    subject = x.value
                    if cancelorder.customer_id == current_user.id:
                        cancelorder.request_cancel = 1,
                        cancelorder.reason_cancel = subject,
                        cancelorder.overallreason = form.messagewhy.data,
                        cancelorder.returncancelage = datetime.utcnow(),
                        db.session.add(cancelorder)

                        # Give user neg exp
                        exppoint(user=cancelorder.customer_id,
                                 price=0,
                                 type=8, quantity=0,
                                 currency=0)
                        db.session.commit()
                        return redirect(url_for('orders.orders_home'))
                    else:
                        return redirect(url_for('index'))
            except:
                flash('Invalid Submit.', 'danger')
                return redirect(url_for('index'))
            return render_template('/service/requestcancel.html',
                                   form=form)
        else:
            flash("Order #" + str(id) + " already shipped", category="danger")
            return redirect(url_for('orders.orders_home'))
    else:
        return redirect(url_for('index'))


@orders.route('/customer-returnorder/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def orders_customer_return(id):
    now = datetime.utcnow()
    returnitem = returnitem_form_factory(orderid=id)
    form = returnitem(request.form)
    order = db.session.query(Vendor_Orders).filter_by(id=id).first()
    if order:
        item = db.session.query(Item_MarketItem).filter(
            Item_MarketItem.id == order.item_id).first()
        msg = db.session.query(
            Service_ShippingSecret).filter_by(orderid=id).first()
        gettracking = db.session.query(
            Service_Tracking).filter_by(sale_id=id).first()
        if order.completed == 0 and order.released == 0 and order.accepted_order == 0 and order.vendor_id != 0:
            if request.method == 'POST':
                if form.validate_on_submit():
                    if order.customer_id == current_user.id:
                        if order.quantity == 1:
                            returnquant = 1
                        else:
                            quant = request.form.getlist(
                                ('quant-' + str(order.id)))
                            # find out quant of whats checked
                            returnquant = quant[0]
                        if int(returnquant) <= int(order.quantity):
                            returnamount = (Decimal(returnquant)
                                            * Decimal(order.price_peritem))
                            form_type_data = form.type.data
                            subject = form_type_data.value
                            order.request_return = 1
                            order.return_quantity = returnquant
                            order.returncancelage = now
                            order.reason_cancel = subject
                            order.overallreason = form.messagewhy.data
                            order.return_amount = returnamount

                            db.session.add(order)

                            notification(type=5, username=order.vendor, user_id=order.vendor_id, salenumber=order.id,
                                         bitcoin=0)
                            db.session.commit()
                            flash("Item Return initiated", category="success")
                            return redirect(url_for('auth.orders_customer_return_instructions', id=id))
                        else:
                            flash("Incorrect amount", category="success")
                    else:
                        return redirect(url_for('index'))
                else:
                    flash("Form Error", category="danger")
        else:
            flash("Order #" + str(id) + "already completed", category="success")
            return redirect(url_for('orders.orders_home'))

        return render_template('/service/requestreturn.html',
                               form=form,
                               order=order,
                               item=item,
                               msg=msg,
                               gettracking=gettracking)
    else:
        return redirect(url_for('index'))
