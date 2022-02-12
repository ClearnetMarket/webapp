from app.common.decorators import \
    ping_user, \
    login_required, \
    website_offline
from flask import render_template, \
    redirect, \
    url_for, \
    flash, \
    request, \
    jsonify

from flask_login import current_user
from app.service import service
from app import db

# models
from app.classes.achievements import \
    UserAchievements, \
    whichAch

from app.classes.auth import User
from app.classes.message import \
    Chat
from app.classes.service import \
    websitefeedback, \
    Issue
from app.classes.profile import \
    StatisticsUser, \
    StatisticsVendor
from app.classes.userdata import \
    Feedback
from app.classes.vendor import \
    Orders
from app.classes.models import \
    btc_cash_Prices

# End Models
from app.service.forms import \
    Feedback, \
    issuewithItem, \
    sendmessageForm, \
    Chatform, \
    feedbackonorderForm, \
    adminhelpserviceform

from datetime import datetime
from sqlalchemy import or_
from app.exppoints import exppoint
from app.achs.a import Grassisgreeneronmyside


@service.route('/')
def customerserviceHome():
    if current_user.is_authenticated:
        # see if orders need to be returned or are disputed
        # customer only
        orders = db.session\
            .query(Orders)\
            .filter(Orders.customer == current_user.username)\
            .filter(or_(Orders.disputed_order == 1, Orders.request_return == 2)).order_by(Orders.age.desc())\
            .all()
        myorderscount = db.session\
            .query(Orders)\
            .filter(Orders.customer == current_user.username)\
            .filter(or_(Orders.disputed_order == 1, Orders.request_return == 2)).order_by(Orders.age.desc())\
            .count()

        # See if user has any active issues for the sidebar
        post = db.session\
            .query(Issue)\
            .filter(Issue.author_id == current_user.id)\
            .order_by(Issue.timestamp.desc())\
            .limit(10)
        thepostcount = post.count()
    else:
        orders = 0
        myorderscount = 0
        post = 0
        thepostcount = 0
    return render_template('/service/customerservicehome.html',
                           orders=orders,
                           myorderscount=myorderscount,
                           post=post,
                           thepostcount=thepostcount)


@service.route('/feedback', methods=['GET', 'POST'])
@website_offline
@login_required
def feedback():
    form = Feedback(request.form)
    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()
    try:
        getcount = db.session\
            .query(websitefeedback)\
            .filter_by(user_id=current_user.id)\
            .count()
    except Exception as e:
        print(str(e))
        getcount = 0
    if request.method == 'POST' and form.validate_on_submit():

        if getcount >= 3:
            return redirect(url_for('index', username=current_user.username))
        else:
            thefeedback = websitefeedback(
                username=user.username,
                user_id=user.id,
                type=form.type.data,
                comment=form.message2.data,
                timestamp=datetime.utcnow()
            )
            db.session.add(thefeedback)
            db.session.commit()
            flash("Feedback submitted.  Exp points given.", category="success")
            flash("We read all feedback. Thank you for your time.",
                  category="success")
            exppoint(user=user.id, price=0, type=4, quantity=0, currency=0)
            Grassisgreeneronmyside(user_id=current_user.id)
            return redirect(url_for('index', username=current_user.username))

    return render_template('/service/feedback.html',
                           form=form,)


@service.route('/disputesandissues', methods=['GET', 'POST'])
@website_offline
def customerservice_disputesquestions():
    try:
        return render_template('/service/subservicePages/servicedisputequestions.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/customerbitcoin', methods=['GET', 'POST'])
@website_offline
def customerservice_bitcoin():
    try:
        return render_template('/service/subservicePages/servicebitcoin.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/shipmentfailure')
@website_offline
def customerservice_shipmentfailure():
    try:
        return render_template('/service/subservicePages/shipfailure.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/cancelitem')
@website_offline
def customerservice_cancelitem():
    try:
        return render_template('/service/subservicePages/servicecancelitem.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/returns')
@website_offline
def customerservice_returnitem():
    try:
        return render_template('/service/subservicePages/servicereturns.html')
    except:

        return jsonify(result={"status": 200})


@service.route('/notrecieved')
@website_offline
def customerservice_notrecieved():
    try:
        return render_template('/service/subservicePages/serviceitemnotrecieved.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/sellerfees')
@website_offline
def customerservice_sellerfees():
    try:
        return render_template('/service/subservicePages/servicesellerfees.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/forgotaccount')
@website_offline
def customerservice_forgotaccount():
    try:
        return render_template('/service/subservicePages/serviceforgotaccount.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/other')
@website_offline
def customerservice_other():
    try:
        return render_template('/service/subservicePages/serviceother.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/customerdispute')
@website_offline
@login_required
def customerservice_dispute():
    try:
        return render_template('/service/customerservicedispute.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/otherfees')
@website_offline
def customerservice_walletfees():
    try:
        return render_template('/service/subservicePages/servicewalletfees.html')
    except:
        return jsonify(result={"status": 200})


@service.route('/item-help/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def helpwithitem(id):
    now = datetime.utcnow()
    issue = issuewithItem(request.form)
    getitem = db.session.query(Orders).filter(Orders.id == id).first()

    if getitem.customer_id == current_user.id:
        if request.method == 'POST' and issue.validate_on_submit():

            try:
                sub = issue.subject.data
                getitem.disputed_order = 1
                getitem.reason_cancel = sub.id
                getitem.private_note = issue.issuebody.data

                db.session.add(getitem)
                db.session.commit()
                flash("Message has been sent.  A representative will be with you. "
                      " Check your notifications.", category="success")
                return redirect(url_for('service.helpwithitem_active', id=getitem.id))
            except Exception as e:
                print(str(e))
                db.session.rollback()
                flash("Form Error", category="danger")
                return redirect(url_for('service.helpwithitem_active', id=getitem.id))

        return render_template('/service/helpwithitem.html',
                               issue=issue,
                               now=now,
                               getitem=getitem,
                               )
    else:
        return redirect(url_for('index', username=current_user.username))


@service.route('/redirect/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def find_item(id):
    """
    This routes the order for the admin
    :param id:
    :return:
    """
    order = db.session.query(Orders).filter_by(id=id).first()
    if order.type == 1:
        return redirect(url_for('service.helpwithitem_active', id=order.id))
    else:
        return redirect(url_for('index', username=current_user.username))


@service.route('/messagecustomerservice', methods=['GET', 'POST'])
@website_offline
@login_required
def customerserviceMessage():
    """
    The home screen for submitting a ticket for support
    IT gets previous tickets, statuses, and allows you to make a new ticket
    :return:
    """
    form = sendmessageForm(request.form)

    # See if user has any active issues for the sidebar
    post = db.session\
        .query(Issue)\
        .filter(Issue.author_id == current_user.id)\
        .order_by(Issue.timestamp.desc())\
        .limit(10)
    thepostcount = post.count()

    if request.method == 'POST':
        if thepostcount <= 10:
            if form.submit.data and form.validate_on_submit():
                addissue = Issue(author=current_user.username,
                                 author_id=current_user.id,
                                 timestamp=datetime.utcnow(),
                                 admin=0,
                                 status=0
                                 )
                db.session.add(addissue)
                db.session.flush()

                post = Chat(
                    orderid=0,
                    author=current_user.username,
                    author_id=current_user.id,
                    timestamp=datetime.utcnow(),
                    body=form.body1.data,
                    admin=0,
                    type=0,
                    issueid=addissue.id
                )
                db.session.add(post)
                db.session.commit()

                flash("Message sent.  A response will be given shortly",
                      category="success")
                return redirect(url_for('service.customerserviceMessage',
                                        username=current_user.username))
            else:
                flash("invalid Captcha", category="danger")
                return redirect(url_for('service.customerserviceMessage',
                                        username=current_user.username))
        else:
            flash("Too many support issues", category="danger")
            return redirect(url_for('service.customerserviceMessage',
                                    username=current_user.username))

    return render_template('/service/msgcustomerservice.html',
                           form=form,
                           post=post,
                           )


@service.route('/needhelpwithissue/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def helpwithissue_active(id):
    """
    The active chat message for support tickets
    The user and admin is present
    :param id:
    :return:
    """
    now = datetime.utcnow()
    postform = Chatform(request.form)
    adminform = adminhelpserviceform(request.form)
    # query the issue
    theissue = db.session\
        .query(Issue)\
        .filter_by(id=id)\
        .first()
    if theissue:
        # get the main chat message
        getchatmsg = db.session\
            .query(Chat)\
            .filter(Chat.issueid == theissue.id,
                    Chat.orderid == 0,
                    Chat.type == 0)\
            .first()

        # set a morderator
        getmod = db.session\
            .query(User)\
            .filter(User.id == theissue.admin)\
            .first()
        if getmod is not None:
            moderator = getmod.username
        else:
            moderator = 0

        if theissue is not None:
            if current_user.id == theissue.author_id or current_user.admin == 1:

                # Get chat messages
                posts = db.session\
                    .query(Chat)\
                    .filter(Chat.issueid == theissue.id)\
                    .order_by(Chat.timestamp.desc())\
                    .filter(Chat.type == 0)
                comments = posts.limit(50)
                if request.method == 'POST':
                    # if user is the messanger or an admin
                    if current_user.id == theissue.author_id:
                        # post the chat message of form validates
                        if postform.post.data and postform.validate_on_submit():
                            try:
                                post = Chat(
                                    orderid=id,
                                    author=current_user.username,
                                    author_id=current_user.id,
                                    timestamp=datetime.utcnow(),
                                    body=postform.bodyofchat.data,
                                    admin=0,
                                    type=0,
                                    issueid=theissue.id
                                )
                                db.session.add(post)
                                db.session.commit()
                                return redirect(url_for('service.helpwithissue_active',
                                                        id=theissue.id))
                            except Exception as e:

                                flash("Form Error", category="danger")
                                db.session.rollback()
                                return redirect(url_for('service.helpwithissue_active',
                                                        id=theissue.id))

                        else:
                            flash("Form Error", category="danger")
                            db.session.rollback()
                            return redirect(url_for('service.helpwithissue_active',
                                                    id=theissue.id))
                    elif current_user.admin == 1:

                        # post the chat message of form validates
                        if postform.post.data:
                            try:
                                post = Chat(
                                    orderid=id,
                                    author=current_user.username,
                                    author_id=current_user.id,
                                    timestamp=datetime.utcnow(),
                                    body=postform.bodyofchat.data,
                                    admin=current_user.id,
                                    type=0,
                                    issueid=theissue.id
                                )
                                db.session.add(post)
                                db.session.commit()
                                return redirect(url_for('service.helpwithissue_active',
                                                        id=theissue.id))
                            except Exception as e:
                                print(str(e))
                                flash("Form Error", category="danger")
                                db.session.rollback()
                                return redirect(url_for('service.helpwithissue_active',
                                                        id=theissue.id))
                        elif adminform.becomeadmin.data:
                            theissue.admin = current_user.id
                            db.session.add(theissue)
                            db.session.commit()
                        elif adminform.delete.data:
                            db.session.delete(theissue)
                            db.session.commit()
                        elif adminform.resolved.data:
                            theissue.status = 1
                            db.session.add(theissue)
                            db.session.commit()
                        else:
                            pass
                        return redirect(url_for('service.helpwithissue_active',
                                                id=theissue.id))
                    else:
                        pass

                return render_template('service/chatroom/help.html',
                                       postform=postform,
                                       adminform=adminform,
                                       now=now,
                                       moderator=moderator,
                                       theissue=theissue,
                                       getchatmsg=getchatmsg,
                                       comments=comments,
                                       getmod=getmod,
                                       user=current_user,
                                       )
            else:
                flash("No Issue", category="danger")
                return redirect(url_for('index'))
        else:
            flash("Not your issue", category="danger")
            return redirect(url_for('index'))
    else:
        flash("No Issue", category="danger")
        return redirect(url_for('index'))


@service.route('/needhelpwithitem/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def helpwithitem_active(id):

    now = datetime.utcnow()

    feedbackform = feedbackonorderForm(request.form)
    postform = Chatform(request.form)
    # get the order
    order = db.session\
        .query(Orders)\
        .filter_by(id=id)\
        .first()
    if current_user.id == order.customer_id or current_user.admin == 1:

        # User
        user = db.session\
            .query(User)\
            .filter_by(id=order.customer_id)\
            .first()
        usergetlevel = db.session\
            .query(UserAchievements)\
            .filter_by(username=user.username)\
            .first()
        userpictureid = str(usergetlevel.level)
        userstats = db.session\
            .query(StatisticsUser)\
            .filter_by(username=user.username)\
            .first()
        level = db.session\
            .query(UserAchievements)\
            .filter_by(username=user.username)\
            .first()
        width = int(level.experiencepoints / 10)
        userach = db.session\
            .query(whichAch)\
            .filter_by(user_id=user.id)\
            .first()
        # vendor
        if order.modid == 0:
            vendor = 0
            vendorach = 0
            vendorstats = 0
            vendorgetlevel = 0
            vendorpictureid = 0
        else:
            vendor = db.session\
                .query(User)\
                .filter_by(id=order.modid)\
                .first()

            vendorstats = db.session\
                .query(StatisticsVendor)\
                .filter_by(vendorid=vendor.id)\
                .first()
            vendorgetlevel = db.session\
                .query(UserAchievements)\
                .filter_by(username=vendor.username)\
                .first()
            vendorpictureid = str(vendorgetlevel.level)
            vendorach = db.session\
                .query(whichAch)\
                .filter_by(user_id=vendor.id)\
                .first()

        # Page Queries
        # Get 20 buys for btc
        posts = db.session.query(Chat)
        posts = posts.filter(Chat.orderid == order.id)
        posts = posts.order_by(Chat.timestamp.desc())
        posts = posts.filter(Chat.type == order.type)
        comments = posts.limit(50)

        btcprice = db.session\
            .query(btc_cash_Prices)\
            .filter(or_(btc_cash_Prices.currency_id == 1,
                    btc_cash_Prices.currency_id == 30,
                    btc_cash_Prices.currency_id == 17,
                    btc_cash_Prices.currency_id == 23,
                    btc_cash_Prices.currency_id == 30,
                    btc_cash_Prices.currency_id == 6,
                    btc_cash_Prices.currency_id == 4,
                        ))\
            .order_by(btc_cash_Prices.currency_id.asc())\
            .all()

        btcprice_cashz = db.session\
            .query(btc_cash_Prices)\
            .filter(or_(btc_cash_Prices.currency_id == 1,
                    btc_cash_Prices.currency_id == 30,
                    btc_cash_Prices.currency_id == 17,
                    btc_cash_Prices.currency_id == 23,
                    btc_cash_Prices.currency_id == 30,
                    btc_cash_Prices.currency_id == 6,
                    btc_cash_Prices.currency_id == 4,
                        ))\

        if request.method == 'POST':
            if current_user.id == order.customer_id or current_user.admin == 1:
                # CHAT
                #
                if postform.post.data and postform.validate_on_submit():
                    try:
                        post = Chat(
                            orderid=order.id,
                            author=current_user.username,
                            author_id=current_user.id,
                            timestamp=datetime.utcnow(),
                            body=postform.bodyofchat.data,
                            admin=0,
                            type=1
                        )
                        db.session.add(post)
                        db.session.commit()
                        return redirect(url_for('service.helpwithitem_active', id=order.id))
                    except Exception:
                        flash("Form Error", category="danger")
                        db.session.rollback()
                        return redirect(url_for('service.helpwithitem_active', id=order.id))

                elif feedbackform.submitfeedback.data:
                    if feedbackform.validate_on_submit():
                        my_id = request.form.get("my_id", "")
                        getitemid = db.session.query(
                            Orders).filter_by(id=my_id).first()
                        if getitemid.customer_id == current_user.id:
                            text_box_value_vendorrating = request.form.get(
                                "vendorrating")
                            text_box_value_item_rating = request.form.get(
                                "item_rating")
                            if text_box_value_vendorrating and text_box_value_item_rating is not None:
                                try:
                                    feed = Feedback(
                                        type=getitemid.type,
                                        sale_id=getitemid.id,
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
                                    db.session.add(feed)

                                    # vendorexp based off score results
                                    exppoint(user=getitemid.vendor_id, price=0, type=7,
                                             quantity=int(text_box_value_vendorrating), currency=0)
                                    # customer exp for giving review based off score results
                                    exppoint(user=current_user.id, price=0, type=3,
                                             quantity=int(text_box_value_vendorrating), currency=0)
                                    db.session.commit()
                                    flash('Feedback submitted.  Exp Points Given for the feedback!.',
                                          'success')

                                    return redirect(url_for('orders.ordershome', username=current_user.username))
                                except Exception as e:
                                    print(str(e))
                                    return redirect(url_for('service.helpwithitem_active', id=order.id))

                            else:
                                flash(
                                    'Invalid Review. Please make sure you filled out '
                                    'the ratings and feedback(longer than 10 characters)',
                                    'danger')
                                return redirect(url_for('orders.ordershome', username=current_user.username))
                        else:
                            flash(
                                'Invalid Review. Please make sure you filled out '
                                'the ratings and feedback(longer than 10 characters)',
                                'danger')
                            return redirect(url_for('orders.ordershome', username=current_user.username))
                    else:
                        flash(
                            'Invalid Review. Please make sure you'
                            ' filled out the ratings and feedback(longer than 10 characters)',
                            'danger')
                        return redirect(url_for('orders.ordershome', username=current_user.username))
                else:
                    return redirect(url_for('orders.ordershome', username=current_user.username))

        return render_template('service/chatroom/helpwithitem.html',
                               user=user,
                               now=now,
                               order=order,
                               userpictureid=userpictureid,
                               usergetlevel=usergetlevel,
                               postform=postform,
                               vendorstats=vendorstats,
                               vendor=vendor,
                               vendorgetlevel=vendorgetlevel,
                               vendorpictureid=vendorpictureid,
                               comments=comments,
                               btcprice=btcprice,
                               btcprice_cashz=btcprice_cashz,
                               userstats=userstats,
                               level=level,
                               width=width,
                               userach=userach,
                               vendorach=vendorach,
                               feedbackform=feedbackform
                               )
    else:
        flash("Trade is currently being traded by other users..", category="success")
        return redirect(url_for('index'))
