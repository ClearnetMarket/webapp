import os
from app import db
from app import UPLOADED_FILES_DEST
from datetime import datetime
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, logout_user, login_user
from flask_paginate import Pagination, get_page_args
from flask import request
from sqlalchemy.orm.exc import UnmappedInstanceError
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from decimal import Decimal
from app.auth import auth
from app.auth.profile_image_resizer import imagespider
from app.common.functions import id_generator_picture1
from app.exppoints import exppoint
from app.achievements.a import newbie
from app.achievements.v import becamevendor
from app.common.functions import mkdir_p, userimagelocation
from app.notification import notification
from app.search.searchfunction import headerfunctions
from app.userdata.views import \
    addtotalItemsBought, \
    addtotalItemsSold, \
    differenttradingpartners_user, \
    differenttradingpartners_vendor, \
    vendortotalmade_btccash, \
    totalspentonitems_btccash, \
    reviewsgiven, \
    reviewsrecieved, \
    affstats

# btc cash work
from app.wallet_bch.wallet_btccash_work import \
    btc_cash_sendCointoclearnet, \
    btc_cash_sendcointoaffiliate, \
    btc_cash_sendCointoUser, \
    btc_cash_create_wallet

from app.common.decorators import \
    ping_user, \
    website_offline, \
    login_required

# forms
from app.auth.forms import searchForm
from app.auth.forms import LoginForm, \
    RegistrationForm, \
    CheckSeed, \
    ChangePasswordForm, \
    myaccount_form_factory, \
    becomeavendor, \
    feedbackonorderForm, \
    requestCancelform, \
    returnitem_form_factory, \
    markasSent, \
    VacationForm, \
    achselectForm, \
    vendorSignup, \
    ConfirmSeed, \
    ChangePinForm, \
    Deleteaccountform
# models
from app.classes.auth import \
    User, \
    UserFees, \
    AccountSeedWords
from app.classes.achievements import \
    UserAchievements, \
    whichAch
from app.classes.affiliate import \
    AffiliateOverview
from app.classes.item import \
    marketItem, \
    ShoppingCartTotal, \
    ShoppingCart
from app.classes.profile import \
    StatisticsUser, \
    StatisticsVendor
from app.classes.service import \
    shippingSecret, \
    Returns, \
    ReturnsTracking, \
    Tracking
from app.classes.models import WordSeeds 
from app.classes.userdata import \
    userHistory, \
    Feedback
from app.classes.vendor import \
    Orders, \
    vendorVerification
from app.classes.wallet_bch import \
    BchUnconfirmed, \
    BchWallet

from app.classes.models import \
    btc_cash_Prices
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only

@auth.route("/logout", methods=["GET"])
def logout():
    try:
        current_user.is_authenticated = False
        logout_user()
    except UnmappedInstanceError:

        return redirect(url_for('index'))
    return redirect(url_for('index'))


@auth.route('/login', methods=['GET', 'POST'])
@website_offline
@ping_user
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(
                username=form.username.data).first()
            if user:
                if user.confirmed == 1:
                    if user is not None:
                        if User.decryptpassword(pwdhash=user.password_hash, password=form.password_hash.data):
                            if user.locked == 0:
                                login_user(user)
                                current_user.is_authenticated()
                                current_user.is_active()
                                # remove fails
                                user.fails = 0
                                db.session.add(user)
                                db.session.commit()

                                return redirect(url_for('index', username=current_user.username))
                            else:
                                flash(
                                    "Account Locked.  Please enter seed to unlock", category="danger")
                                return redirect(url_for('auth.login'))
                        else:
                            flash("Please retry username and password",
                                  category="danger")
                            x = int(user.fails)
                            y = x + 1
                            user.fails = y
                            db.session.add(user)
                            db.session.commit()
                            if int(user.fails) == 5:
                                user.locked = 1
                                db.session.add(user)
                                db.session.commit()
                                return redirect(url_for('auth.login'))
                            else:
                                return redirect(url_for('auth.login'))
                    else:
                        flash("Please retry username/password",
                              category="danger")
                        return redirect(url_for('auth.login'))
                else:
                    flash("Account was not confirmed with seed", category="danger")
                    return redirect(url_for('auth.confirmseed'))
            else:
                flash("Please retry username/password", category="danger")
                return redirect(url_for('auth.login'))
        else:
            flash("Please retry username/password. Form Error", category="danger")
            return redirect(url_for('auth.login'))

    return render_template('/auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
@website_offline
def register():
    form = RegistrationForm()
    shard = 1

    if request.method == 'POST' and form.validate_on_submit():

        now = datetime.utcnow()
        cryptedpwd = User.cryptpassword(password=form.password.data)
        cryptedpin = User.cryptpassword(password=form.walletpin.data)
        namefull = form.country.data
        name = namefull.numericcode
        currencyfull = form.currency.data
        cur = currencyfull.code

        # add user to db
        new_user = User(
            username=form.username.data,
            email='',
            password_hash=cryptedpwd,
            member_since=now,
            wallet_pin=cryptedpin,
            profileimage='user-unknown.png',
            stringuserdir=0,
            bio='',
            country=name,
            currency=cur,
            vendor_account=0,
            selling_from=0,
            last_seen=now,
            admin=0,
            admin_role=0,
            dispute=0,
            fails=0,
            locked=0,
            vacation=0,
            shopping_timer=now,
            lasttraded_timer=now,
            shard=shard,
            usernode=0,
            affiliate_account=0,
            confirmed=0,
            passwordpinallowed=0
        )

        db.session.add(new_user)
        db.session.flush()

        # create user stats
        stats = StatisticsUser(
            username=new_user.username,
            totalitemsbought=0,
            totalbtcspent=0,
            totalbtcrecieved=0,
            totalbtccashspent=0,
            totalbtccashrecieved=0,
            totalreviews=0,
            startedbuying=now,
            diffpartners=0,
            totalachievements=0,
            user_id=new_user.id,
            userrating=0,
            totaltrades=0,
            disputecount=0,
            itemsflagged=0,
            totalusdspent=0,
        )

        # create which achs they pick
        achselect = whichAch(
            user_id=new_user.id,
            ach1='0',
            ach2='0',
            ach3='0',
            ach4='0',
            ach5='0',
            ach1_cat='0',
            ach2_cat='0',
            ach3_cat='0',
            ach4_cat='0',
            ach5_cat='0',
        )

        # create users achs
        ach = UserAchievements(
            user_id=new_user.id,
            username=new_user.username,
            experiencepoints=0,
            level=1,
        )

        # create browser history
        browserhistory = userHistory(
            user_id=new_user.id,
            recentcat1=1,
            recentcat1date=now,
            recentcat2=2,
            recentcat2date=now,
            recentcat3=3,
            recentcat3date=now,
            recentcat4=4,
            recentcat4date=now,
            recentcat5=7,
            recentcat5date=now,
        )

        # create shoppingcart for user
        newcart = ShoppingCartTotal(
            customer=new_user.id,
            btc_cash_sumofitem=0,
            btc_cash_price=0,
            shipping_btc_cashprice=0,
            total_btc_cash_price=0,
            percent_off_order=0,
            btc_cash_off=0,
        )

        setfees = UserFees(user_id=new_user.id,
                           buyerfee=0,
                           buyerfee_time=now,
                           vendorfee=2,
                           vendorfee_time=now,
                           )
                           
        db.session.add(setfees)
        strid = str(new_user.id)
        new_user.stringuserdir = strid + '/'

        # add to db
        db.session.add(ach)
        db.session.add(browserhistory)
        db.session.add(achselect)
        db.session.add(stats)
        db.session.add(newcart)

        # creates bitcoin cash wallet in db
        btc_cash_create_wallet(user_id=new_user.id)

        newbie(user_id=new_user.id)

        # make a user a directory
        getuserlocation = userimagelocation(user_id=new_user.id)
        userfolderlocation = os.path.join(UPLOADED_FILES_DEST,
                                          "user",
                                          getuserlocation,
                                          str(new_user.id))
        mkdir_p(path=userfolderlocation)

        # login new user
        login_user(new_user)
        current_user.is_authenticated()
        current_user.is_active()

        # Commit all to database
        db.session.commit()

        flash("Successfully Registered", category="success")
        return redirect(url_for('auth.createaccountseed'))

    return render_template('/auth/register.html', form=form)


@auth.route('/accountseed', methods=["GET"])
@login_required
def createaccountseed():
    import random
    # get the current user
    user = db.session.query(User).filter_by(id=current_user.id).first()

    # see if user seed created..
    userseed = db.session \
        .query(AccountSeedWords) \
        .filter(user.id == AccountSeedWords.user_id) \
        .first()

    if request.method == 'GET':
        if userseed is None:
            # created the wallet seed
            word_list = []

            get_words = db.session.query(WordSeeds).order_by(func.random()).limit(6)
            for f in get_words:
                word_list.append(f.text)
                print(f.text)
            word00 = str(word_list[0]).lower()
            word01 = str(word_list[1]).lower()
            word02 = str(word_list[2]).lower()
            word03 = str(word_list[3]).lower()
            word04 = str(word_list[4]).lower()
            word05 = str(word_list[5]).lower()

            addseedtodb = AccountSeedWords(user_id=user.id,
                                        word00=word00,
                                        word01=word01,
                                        word02=word02,
                                        word03=word03,
                                        word04=word04,
                                        word05=word05,
                                        )
            db.session.add(addseedtodb)
            db.session.commit()

        else:
            word00 = userseed.word00
            word01 = userseed.word01
            word02 = userseed.word02
            word03 = userseed.word03
            word04 = userseed.word04
            word05 = userseed.word05

        return render_template('auth/accountseed.html',
                            word00=word00,
                            word01=word01,
                            word02=word02,
                            word03=word03,
                            word04=word04,
                            word05=word05,
                            )


@auth.route('/accountseedconfirm', methods=["GET", "POST"])
@website_offline
@login_required
def confirmseed():

    form = ConfirmSeed()
    
    # get the user
    user = db.session\
        .query(User)\
        .filter(current_user.id == User.id)\
        .first()

    if user.confirmed == 1:
        flash("You have already been confirmed", category="danger")
        return redirect(url_for('index'))
    if request.method == 'POST':
        # get the users seed
        userseed = db.session.query(AccountSeedWords) \
            .filter(user.id == AccountSeedWords.user_id)\
            .first()

        w00 = form.seedanswer0.data
        w01 = form.seedanswer1.data
        w02 = form.seedanswer2.data
        w03 = form.seedanswer3.data
        w04 = form.seedanswer4.data
        w05 = form.seedanswer5.data

        if w00 == userseed.word00 and \
            w01 == userseed.word01 and \
            w02 == userseed.word02 and \
            w03 == userseed.word03 and \
            w04 == userseed.word04 and \
            w05 == userseed.word05:

            user.confirmed = 1

            db.session.add(user)
            db.session.commit()

            flash("Account Confirmed.", category="danger")
            return redirect(url_for('index'))
        else:
            flash("Incorrect Seed Entry", category="danger")
            return redirect(url_for('auth.confirmseed'))

    if request.method == 'GET':
        return render_template('/auth/confirmseed.html', form=form)


def deleteprofileimage(id, img, type):
    if current_user.id == id:
        user = db.session \
            .query(User)\
            .filter(User.id == id)\
            .first()
        user_id = str(id)
        userimg1 = str(img)
        userimg2 = str(img)[:-9] + '.jpg'
        usernodelocation = str(user.usernode)
        file0 = os.path.join(UPLOADED_FILES_DEST, "user",
                             usernodelocation, user_id, userimg1)
        file1 = os.path.join(UPLOADED_FILES_DEST, "user",
                             usernodelocation, user_id, userimg2)
        try:
            os.remove(file0)
            os.remove(file1)
        except Exception:
            user.profileimage = 'user-unknown.png'
            db.session.add(user)
            db.session.commit()
        if type == 0:
            pass
        elif type == 1:
            user.profileimage = 'user-unknown.png'
            db.session.add(user)
            db.session.commit()
        else:
            pass
    else:
        return redirect(url_for('index'))


@auth.route('/my-account/', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def myAccount():
    now = datetime.utcnow()
    title = 'My Account'

    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()

    id_pic1 = id_generator_picture1()
    vacform = VacationForm()
    myaccountform = myaccount_form_factory(user)

    form = myaccountform(
        CombinedMultiDict((request.files, request.form)),
        Bio=user.bio,
        country=user.country,
    )

    if request.method == 'POST':

        if vacform.Vacation.data:
            return redirect(url_for('vendor.vacation', username=current_user.username))

        if form.delete.data:
            deleteprofileimage(id=user.id, img=user.profileimage, type=1)
            return redirect(url_for('auth.myAccount', username=current_user.username))

        if form.submit.data and form.validate_on_submit():
            userlocation = os.path.join(
                UPLOADED_FILES_DEST, "user", str(user.usernode), (str(user.id)))

            def image1():
                if form.imageprofile.data:
                    try:
                        mkdir_p(path=userlocation)
                        deleteprofileimage(
                            id=current_user.id, img=current_user.profileimage, type=0)
                        filename = secure_filename(
                            form.imageprofile.data.filename)
                        # saves it to location
                        profileimagefilepath = os.path.join(
                            userlocation, filename)
                        form.imageprofile.data.save(profileimagefilepath)
                        # RENAMING FILE
                        # split file name and ending
                        filenamenew, file_extension = os.path.splitext(
                            profileimagefilepath)
                        # gets new 64 digit filename
                        newfileName = id_pic1 + file_extension
                        # puts new name with ending
                        filenamenewfull = filenamenew + file_extension
                        # gets aboslute path of new file
                        newfileNameDestination = os.path.join(
                            userlocation, newfileName)
                        # renames file
                        os.rename(filenamenewfull, newfileNameDestination)

                        dbname = id_pic1 + "_125x.jpg"
                    except Exception as e:
                        flash("Error WIth Picture Submission",
                              category="success")
                        return redirect(url_for('auth.myAccount', username=current_user.username))
                    if form.imageprofile.data.filename:
                        x1 = dbname
                        # add profile to db
                        user.profileimage = x1
                        db.session.add(user)

                    else:
                        x1 = "user-unknown.png"
                    imagespider(base_path=userlocation)
                    return x1

                else:
                    pass

            image1()
            # get origin country query
            origincountryfull = form.origincountry1.data
            origincountry = origincountryfull.numericcode
            currencyfull = form.currency1.data
            cur = currencyfull.code
            user.currency = cur,
            user.bio = form.Bio.data,
            user.country = origincountry,

            db.session.add(user)
            db.session.commit()
            flash("Information Updated", category="success")
            return redirect(url_for('auth.myAccount',
                                    username=current_user.username))
        else:
            flash("Form Error", category="danger")
            return redirect(url_for('auth.myAccount',
                                    username=current_user.username))
    return render_template('auth/account/myAccount.html',
                           title=title,
                           form=form,
                           now=now,
                           user=user,
                           vacform=vacform)


@auth.route('/sell', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def becomeVendor():
    if current_user.vendor_account == 0:
        form = becomeavendor(request.form)
        if request.method == 'POST':
            return redirect(url_for('auth.setupAccount'))
        return render_template('auth/account/vendorintro.html', form=form)
    else:
        return redirect(url_for('vendor.tradeOptions', username=current_user.username))


@auth.route('/vendor-signup', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def setupAccount():
    now = datetime.utcnow()
    form = vendorSignup(request.form)
    user = db.session \
        .query(User) \
        .filter(User.id == current_user.id) \
        .first()

    if request.method == 'POST':
        if form.validate_on_submit():
            if user.username == form.username.data:
                if form.agreement.data is True:

                    user.vendor_account = 1,
                    user.sellingfrom = form.country.data

                    stats = StatisticsVendor(
                        username=user.username,
                        vendorid=user.id,
                        totalsales=0,
                        totalbtcspent=0,
                        totalbtcrecieved=0,
                        totalbtccashspent=0,
                        totalbtccashrecieved=0,
                        totalreviews=0,
                        startedselling=now,
                        vendorrating=0,
                        diffpartners=0,
                        totaltrades=0,
                        disputecount=0,
                        beenflagged=0,
                        avgitemrating=0,
                        totalusdmade=0,
                    )

                    addverify = vendorVerification(
                        vendor_id=user.id,
                        vendor_level=0,
                        timestamp=now,
                        amount=0
                    )

                    db.session.add(stats)
                    db.session.add(user)
                    db.session.add(addverify)

                    # add achievemenets
                    becamevendor(user_id=user.id)
                    db.session.commit()
                    flash("Welcome fellow crypto lover.  Here you can get vendor verification.  Its optional!",
                          category="success")
                    return redirect(url_for('vendor.vendorverification'))
                else:
                    flash("Please accept the agreement", category="danger")
                    return redirect(url_for('auth.setupAccount'))
            else:
                flash("invalid username", category="danger")
                return redirect(url_for('auth.setupAccount'))
        else:
            flash(form.errors, category="danger")
            return redirect(url_for('auth.setupAccount'))

    return render_template('/auth/account/setupAccount.html', form=form)


@auth.route('/order-tracking/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def orders_viewtracking(id):
    now = datetime.utcnow()
    form = searchForm()
    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()
    order = db.session\
        .query(Orders)\
        .filter_by(id=id)\
        .first()
    if order:
        msg = db.session\
            .query(shippingSecret)\
            .filter_by(orderid=id)\
            .first()
        tracking = db.session\
            .query(Tracking)\
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


@auth.route('/order-customerservice', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def orders_customerservice():
    return redirect(url_for('auth.setupAccount'))


@auth.route('/customer-returninstructions/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def customerOrders_returninstructions(id):
    now = datetime.utcnow()
    trackingform = markasSent(request.form)

    order = db.session\
        .query(Orders)\
        .filter_by(id=id)\
        .first()
    if order:
        if order.customer_id == current_user.id or order.vendor_id == current_user.id:
            # item
            getitem = db.session\
                .query(marketItem)\
                .filter(marketItem.id == order.item_id)\
                .first()
            vendortracking = db.session\
                .query(Tracking)\
                .filter_by(sale_id=id)\
                .first()
            # delete return address
            returninfo = db.session\
                .query(Returns)\
                .filter_by(ordernumber=id)\
                .first()
            # delete return tracking
            returntracking = db.session\
                .query(ReturnsTracking)\
                .filter_by(ordernumber=id)\
                .first()
            # customer tracking address
            msg = db.session\
                .query(shippingSecret)\
                .filter_by(orderid=id)\
                .first()
            gettracking = db.session\
                .query(Tracking)\
                .filter_by(sale_id=id)\
                .first()
            # Customer Return address check if added
            # if 0 no address added
            # if 1 address added

            returns = db.session\
                .query(Returns)\
                .filter_by(ordernumber=order.id)\
                .first()
            returnscount = db.session\
                .query(Returns)\
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
                        addnewreturn = ReturnsTracking(
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
                        return redirect(url_for('auth.customerOrders_returninstructions', id=id))
                    except Exception as e:
                        flash(str(e), 'danger')
                        flash('Invalid Submit.', 'danger')
                        return redirect(url_for('auth.customerOrders_returninstructions', id=id))

                return redirect(url_for('auth.customerOrders_returninstructions', id=id))

            return render_template('/vendor/vieworder.html',
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


@auth.route('/auth-achievements-all/', methods=['GET', 'POST'])
@website_offline
def achievements_all():
    title = current_user.username + "'s Achievements"

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

    x, size = row2dict(row=db.session
                       .query(UserAchievements)
                       .filter_by(user_id=current_user.id)
                       .first())
    return render_template('/auth/userachievements/achievementsall.html',
                           x=x,
                           size=size,
                           title=title
                           )


@auth.route('/auth-achievements-coin/', methods=['GET', 'POST'])
@website_offline
def achievements_coin():
    title = current_user.username + "'s Achievements"

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
    x, size = row2dict(row=db.session
                       .query(UserAchievements)
                       .filter_by(user_id=current_user.id)
                       .first())

    return render_template('/auth/userachievements/achievementscoin.html',
                           x=x,
                           size=size,
                           title=title
                           )


@auth.route('/auth-achievements-common/', methods=['GET', 'POST'])
@website_offline
def achievements_common():
    title = current_user.username + "'s Achievements"

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
    x, size = row2dict(row=db.session
                       .query(UserAchievements)
                       .filter_by(user_id=current_user.id)
                       .first())
    return render_template('/auth/userachievements/achievementscommon.html',
                           x=x,
                           size=size,
                           title=title
                           )


@auth.route('/auth-achievements-experience/', methods=['GET', 'POST'])
@website_offline
def achievements_experience():
    title = current_user.username + "'s Achievements"

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
    x, size = row2dict(row=db.session
                       .query(UserAchievements)
                       .filter_by(user_id=current_user.id)
                       .first())
    return render_template('/auth/userachievements/achievementsExperience.html',
                           x=x,
                           size=size,
                           title=title
                           )


@auth.route('/auth-achievements-unique/', methods=['GET', 'POST'])
@website_offline
def achievements_unique():
    title = current_user.username + "'s Achievements"

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
    x, size = row2dict(row=db.session
                       .query(UserAchievements)
                       .filter_by(user_id=current_user.id)
                       .first())
    return render_template('/auth/userachievements/achievementsunique.html',
                           x=x,
                           size=size,
                           title=title
                           )


@auth.route('/auth-achievements-customer/', methods=['GET', 'POST'])
@website_offline
def achievements_customer():
    title = current_user.username + "'s Achievements"

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
                if nousername in key:
                    if nodate not in key:
                        if nolevel not in key:
                            if noid not in key:
                                if nouser_id not in key:
                                    if noexp not in key:
                                        solutions.append(key)
        x = solutions
        size = len(x)
        return x, size

    x, size = row2dict(row=db.session
                       .query(UserAchievements)
                       .filter_by(user_id=current_user.id)
                       .first())
    return render_template('/auth/userachievements/achievementscustomer.html',
                           x=x,
                           size=size,
                           title=title
                           )


@auth.route('/auth-achievements-vendor/', methods=['GET', 'POST'])
@website_offline
def achievements_vendor():
    title = current_user.username + "'s Achievements"

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
                if nodate not in key:
                    if nousername in key:
                        if nolevel not in key:
                            if noid not in key:
                                if nouser_id not in key:
                                    if noexp not in key:
                                        solutions.append(key)
        x = solutions
        size = len(x)
        return x, size

    x, size = row2dict(row=db.session
                       .query(UserAchievements)
                       .filter_by(user_id=current_user.id)
                       .first())
    return render_template('/auth/userachievements/achievementsvendor.html',
                           x=x,
                           size=size,
                           title=title
                           )


@auth.route('/select-achievements/', methods=['GET', 'POST'])
@website_offline
def selectuserAchs():
    title = "My Achievements"
    form = achselectForm()
    now = datetime.utcnow()
    specificach = db.session.query(whichAch).filter_by(
        user_id=current_user.id).first()
    if current_user.vendor_account == 0:
        user = db.session.query(User).filter_by(
            username=current_user.username).first()
        usergetlevel = db.session.query(UserAchievements).filter_by(
            username=user.username).first()
        userpictureid = str(usergetlevel.level)
        userwallet = db.session.query(
            BchWallet).filter_by(user_id=user.id).first()
        userstats = db.session.query(StatisticsUser).filter_by(
            username=user.username).first()

        level = db.session.query(UserAchievements).filter_by(
            username=user.username).first()
        width = int(level.experiencepoints / 10)
        userach = db.session.query(whichAch).filter_by(
            user_id=current_user.id).first()
        vendor = 0
        vendorwallet = 0
        vendorstats = 0
        vendorgetlevel = 0
        vendorpictureid = 0
        vendorach = 0
    else:
        # vendor
        vendor = db.session\
            .query(User)\
            .filter_by(id=current_user.id)\
            .first()
        vendorwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=vendor.id)\
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
            .filter_by(user_id=current_user.id)\
            .first()

        user = 0
        usergetlevel = 0
        userpictureid = 0
        userwallet = 0
        userstats = 0
        userach = 0

        level = 0
        width = 0

    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        my_none = '1'
        nodate = 'date'
        noid = 'id'
        nolevel = 'level'
        nouser_id = 'user_id'
        noexp = 'experiencepoints'
        solutions = []
        for key, value in d.items():

            if my_none in value:
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
        UserAchievements).filter_by(user_id=current_user.id).first())

    if request.method == "POST":
        if form.selectone.data:
            if form.ach1.data == specificach.ach2 \
                    or form.ach1.data == specificach.ach3 \
                    or form.ach1.data == specificach.ach4 \
                    or form.ach1.data == specificach.ach5:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('auth.selectuserAchs'))
            else:

                full = form.ach1.data
                if full in x:
                    cat = full[0]
                    specificach.ach1 = form.ach1.data,
                    specificach.ach1_cat = cat,

                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('auth.selectuserAchs'))

        elif form.selecttwo.data:
            if form.ach2.data == specificach.ach1 \
                    or form.ach2.data == specificach.ach3 \
                    or form.ach2.data == specificach.ach4 \
                    or form.ach2.data == specificach.ach5:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('auth.selectuserAchs'))
            else:
                full = form.ach2.data
                if full in x:
                    cat = full[0]
                    specificach.ach2 = form.ach2.data,
                    specificach.ach2_cat = cat,
                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('auth.selectuserAchs'))
        elif form.selectthree.data:
            if form.ach3.data == specificach.ach2 \
                    or form.ach3.data == specificach.ach1 \
                    or form.ach3.data == specificach.ach4 \
                    or form.ach3.data == specificach.ach5:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('auth.selectuserAchs'))
            else:
                full = form.ach3.data
                if full in x:
                    cat = full[0]
                    specificach.ach3 = form.ach3.data,
                    specificach.ach3_cat = cat,
                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('auth.selectuserAchs'))

        elif form.selectfour.data:
            if form.ach4.data == specificach.ach2 \
                    or form.ach4.data == specificach.ach3 \
                    or form.ach4.data == specificach.ach1 \
                    or form.ach4.data == specificach.ach5:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('auth.selectuserAchs'))
            else:
                full = form.ach4.data
                if full in x:
                    cat = full[0]
                    specificach.ach4 = form.ach4.data,
                    specificach.ach4_cat = cat,
                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('auth.selectuserAchs'))
        elif form.selectfive.data:
            if form.ach5.data == specificach.ach2 \
                    or form.ach5.data == specificach.ach3 \
                    or form.ach5.data == specificach.ach4 \
                    or form.ach5.data == specificach.ach1:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('auth.selectuserAchs'))
            else:
                full = form.ach5.data
                if full in x:
                    cat = full[0]
                    specificach.ach5 = form.ach5.data,
                    specificach.ach5_cat = cat,

                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('auth.selectuserAchs'))

        elif form.deleteone.data:
            specificach.ach1 = '0',
            specificach.ach1_cat = '0',
            db.session.add(specificach)
            db.session.commit()

        elif form.deletetwo.data:
            specificach.ach2 = '0',
            specificach.ach2_cat = '0',
            db.session.add(specificach)
            db.session.commit()

        elif form.deletethree.data:
            specificach.ach3 = '0',
            specificach.ach3_cat = '0',
            db.session.add(specificach)
            db.session.commit()

        elif form.deletefour.data:
            specificach.ach4 = '0',
            specificach.ach4_cat = '0',
            db.session.add(specificach)
            db.session.commit()

        elif form.deletefive.data:
            specificach.ach5 = '0',
            specificach.ach5_cat = '0',
            db.session.add(specificach)
            db.session.commit()
        else:
            pass

    return render_template('/auth/userachievements/achievementscustomize.html',
                           x=x,
                           size=size,
                           title=title,
                           form=form,
                           specificach=specificach,
                           user=user,
                           now=now,
                           usergetlevel=usergetlevel,
                           userpictureid=userpictureid,
                           userwallet=userwallet,
                           userstats=userstats,
                           width=width,
                           level=level,
                           vendor=vendor,
                           vendorwallet=vendorwallet,
                           vendorstats=vendorstats,
                           vendorgetlevel=vendorgetlevel,
                           vendorpictureid=vendorpictureid,
                           userach=userach,
                           vendorach=vendorach
                           )


@auth.route('/order-cancel/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def orders_cancelorder(id):
    now = datetime.utcnow()
    try:
        getorder = db.session.query(Orders).filter_by(id=id).first()
        if getorder:
            msg = db.session.query(
                shippingSecret).filter_by(orderid=id).first()
            gettracking = db.session.query(
                Tracking).filter_by(sale_id=id).first()
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
                        getitem = db.session.query(marketItem).filter(
                            getorder.item_id == marketItem.id).first()
                        x = getitem.itemcount
                        y = getorder.quantity
                        z = x + y
                        getitem.itemcount = z

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
                    return redirect(url_for('auth.orders'))
                else:
                    flash("Order #" + str(id) +
                          " cannot be processed with request", category="danger")
                    return redirect(url_for('auth.orders'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    except:
        return redirect(url_for('auth.orders'))


@auth.route('/order-recieved/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def orders_markasrecieved(id):

    now = datetime.utcnow()
    try:
        getorder = db.session.query(Orders).filter_by(id=id).first()
        physicalitemfee = getorder.fee
        if getorder:
            if getorder.customer_id == current_user.id:
                if getorder.completed == 0 and getorder.released == 0 and getorder.vendor_id != 0:
                    if getorder.waiting_order == 1 or getorder.accepted_order == 1:

                        shiprice = (Decimal(getorder.shipping_price) +
                                    Decimal(getorder.price) - getorder.fee)
                        msg = db.session.query(shippingSecret).filter_by(
                            orderid=getorder.id).first()
                        gettracking = db.session.query(Tracking).filter_by(
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
                                .query(AffiliateOverview) \
                                .filter(AffiliateOverview.promocode == getorder.affiliate_code)\
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
                            affstats(user_id=getpromo.user_id,
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
                        totalspentonitems_btccash(user_id=getorder.customer_id,
                                                  howmany=1,
                                                  amount=getorder.price
                                                  )

                        # BTC CASH recieved by vendor
                        vendortotalmade_btccash(user_id=getorder.vendor_id,
                                                amount=shiprice
                                                )

                        # Add total items bought
                        addtotalItemsBought(
                            user_id=getorder.customer_id, howmany=getorder.quantity)

                        # add total sold to vendor
                        addtotalItemsSold(
                            user_id=getorder.vendor_id, howmany=getorder.quantity)

                        # add diff trading partners
                        differenttradingpartners_user(
                            user_id=getorder.customer_id, otherid=getorder.vendor_id)

                        differenttradingpartners_vendor(
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
                        return redirect(url_for('auth.orders'))
                    else:
                        flash("Order #" + str(id) +
                              ": Cannot Finalize", category="success")
                        return redirect(url_for('auth.orders'))
                else:
                    flash("Order #" + str(id) +
                          " already completed", category="success")
                    return redirect(url_for('auth.orders'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    except Exception as e:
        print(str(e))
        return redirect(url_for('auth.orders'))


@auth.route('/order-requestcancel/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def orders_requestcancelorder(id):
    cancelorder = db.session.query(Orders).filter_by(id=id).first()
    if cancelorder:
        if cancelorder.accepted_order == 1 \
                and cancelorder.completed == 0 \
                and cancelorder.vendor_id != 0 \
                and cancelorder.released == 0:
            try:
                form = requestCancelform(request.form)
                cancelorder = db.session.query(Orders).filter_by(id=id).first()
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
                        return redirect(url_for('auth.orders'))
                    else:
                        return redirect(url_for('index'))
            except:
                flash('Invalid Submit.', 'danger')
                return redirect(url_for('index'))
            return render_template('/service/requestcancel.html',
                                   form=form)
        else:
            flash("Order #" + str(id) + " already shipped", category="danger")
            return redirect(url_for('auth.orders'))
    else:
        return redirect(url_for('index'))


@auth.route('/customer-returnorder/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def customerOrders_return(id):
    now = datetime.utcnow()
    returnitem = returnitem_form_factory(orderid=id)
    form = returnitem(request.form)
    order = db.session.query(Orders).filter_by(id=id).first()
    if order:
        item = db.session.query(marketItem).filter(
            marketItem.id == order.item_id).first()
        msg = db.session.query(shippingSecret).filter_by(orderid=id).first()
        gettracking = db.session.query(Tracking).filter_by(sale_id=id).first()
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
                            return redirect(url_for('auth.customerOrders_returninstructions', id=id))
                        else:
                            flash("Incorrect amount", category="success")
                    else:
                        return redirect(url_for('index'))
                else:
                    flash("Form Error", category="danger")
        else:
            flash("Order #" + str(id) + "already completed", category="success")
            return redirect(url_for('auth.orders'))

        return render_template('/service/requestreturn.html',
                               form=form,
                               order=order,
                               item=item,
                               msg=msg,
                               gettracking=gettracking)
    else:
        return redirect(url_for('index'))


@auth.route('/orders', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def orders():
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

    # forms
    formsearch = searchForm()

    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()

    # PEr Page tells how many search results pages
    per_page = 10
    inner_window = 1  # search bar at bottom used for .. lots of pages
    outer_window = 1  # search bar at bottom used for .. lots of pages

    user = db.session.query(User).filter_by(
        username=current_user.username).first()

    btc_cash_price = db.session.query(btc_cash_Prices).all()

    myorders = db.session.query(Orders)
    myorders = myorders.filter((Orders.customer_id == current_user.id))
    myorders = myorders.filter(Orders.vendor_id != 0)
    myorders = myorders.order_by(Orders.age.desc())
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
        if formsearch.search.data and formsearch.validate_on_submit():
            # cats
            categoryfull = formsearch.category.data
            cat = categoryfull.id

            # catch dynamic variables
            if formsearch.searchString.data == '' and cat == 0:
                return redirect(url_for('index'))

            if formsearch.searchString.data == '':
                formsearch.searchString.data = cat

            return redirect(url_for('search.searchMaster',
                                    searchterm=formsearch.searchString.data,
                                    function=cat,

                                    ))

        if feedbackform.submitfeedback.data:
            if feedbackform.validate_on_submit():

                my_id = request.form.get("my_id", "")
                getitemid = db.session.query(
                    Orders).filter_by(id=my_id).first()

                if getitemid.customer_id == current_user.id:
                    if getitemid.feedback == 0:
                        if getitemid.type == 3:
                            text_box_value_vendorrating = request.form.get(
                                "vendorrating")
                            text_box_value_itemrating = 0
                        else:
                            text_box_value_vendorrating = request.form.get(
                                "vendorrating")
                            text_box_value_itemrating = request.form.get(
                                "itemrating")
                        if text_box_value_vendorrating and text_box_value_itemrating is not None:
                            if (1 <= int(text_box_value_vendorrating) <= 5) \
                                    and (1 <= int(text_box_value_itemrating) <= 5):
                                add = Feedback(
                                    type=getitemid.type,
                                    sale_id=getitemid.id,
                                    timestamp=now,
                                    vendorname=getitemid.vendor,
                                    vendorid=getitemid.vendor_id,
                                    customername=current_user.username,
                                    author_id=current_user.id,
                                    comment=feedbackform.feedbacktext.data,
                                    itemrating=text_box_value_itemrating,
                                    vendorrating=text_box_value_vendorrating,
                                    item_id=getitemid.item_id,
                                    addedtodb=0,
                                )
                                getitemid.feedback = 1

                                db.session.add(add)
                                db.session.add(getitemid)

                                # add a review
                                reviewsgiven(user_id=user.id)
                                reviewsrecieved(user_id=getitemid.vendor_id)

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
                                return redirect(url_for('auth.orders'))
                            else:
                                flash('Invalid Review. '
                                      'Please make sure you filled out the ratings and feedback. '
                                      'Must be Longer than 10 characters)',
                                      category="danger")
                                return redirect(url_for('auth.orders'))

                        else:
                            flash('Invalid Review. '
                                  'Please make sure you filled out the ratings and feedback. '
                                  'Must be longer than 10 characters)',
                                  category="danger")
                            return redirect(url_for('auth.orders'))
                    else:
                        flash('Item already reviewed',
                              category="danger")
                        return redirect(url_for('auth.orders'))
                else:
                    flash('Invalid User.',
                          category="danger")
                    return redirect(url_for('auth.orders'))
            else:
                flash('Invalid Review.'
                      'Please make sure you filled out the ratings and feedback. longer than 10 characters',
                      category="danger")
                return redirect(url_for('auth.orders'))

    return render_template('/auth/orders/orders.html',
                           form=formsearch,
                           # header stuff
                           btc_cash_price=btc_cash_price,
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


@auth.route('/lost-password', methods=['GET', 'POST'])
def retrievepassword():

    form = CheckSeed()
    if request.method == 'POST':
        if form.validate_on_submit():
            # get the user based off of form
            user = db.session.query(User).filter_by(
                username=form.username.data).first()
            # match the seed to the user
            userseed = db.session.query(AccountSeedWords) \
                .filter(user.id == AccountSeedWords.user_id).first()

            w00 = form.seedanswer0.data
            w01 = form.seedanswer1.data
            w02 = form.seedanswer2.data
            w03 = form.seedanswer3.data
            w04 = form.seedanswer4.data
            w05 = form.seedanswer5.data

            if w00 == userseed.word00 and \
                    w01 == userseed.word01 and \
                    w02 == userseed.word02 and \
                    w03 == userseed.word03 and \
                    w04 == userseed.word04 and \
                    w05 == userseed.word05:

                user.passwordpinallowed = 1
                db.session.add(user)
                db.session.commit()

                # login  user
                login_user(user)
                current_user.is_authenticated()
                current_user.is_active()

                flash("Account Confirmed.", category="success")
                return redirect(url_for('auth.changepassword'))
            else:
                flash("Incorrect Seed Entry", category="danger")
                return redirect(url_for('auth.retrievepassword'))

    return render_template('/auth/security/lostPassword.html',
                           form=form
                           )


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def changepassword():

    form = ChangePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(id=current_user.id).first()
            user = User.query.filter_by(id=current_user.id).first()
            cryptedpwd = User.cryptpassword(password=form.newpasswordtwo.data)

            user.password_hash = cryptedpwd
            user.passwordpinallowed = 0

            db.session.add(user)
            db.session.commit()

            flash('Your password has been updated!', category="success")
            return redirect(url_for('index'))

    return render_template('/auth/security/newpassword.html',
                           form=form
                           )


@auth.route('/lost-pin', methods=['GET', 'POST'])
@website_offline
def retrievepin():
    form = CheckSeed()
    if request.method == 'POST':
        if form.validate_on_submit():
            # get the user based off of form
            user = db.session.query(User).filter_by(
                username=form.username.data).first()
            # match the seed to the user
            userseed = db.session.query(AccountSeedWords) \
                .filter(user.id == AccountSeedWords.user_id).first()

            w00 = form.seedanswer0.data
            w01 = form.seedanswer1.data
            w02 = form.seedanswer2.data
            w03 = form.seedanswer3.data
            w04 = form.seedanswer4.data
            w05 = form.seedanswer5.data

            if w00 == userseed.word00 and \
                    w01 == userseed.word01 and \
                    w02 == userseed.word02 and \
                    w03 == userseed.word03 and \
                    w04 == userseed.word04 and \
                    w05 == userseed.word05:

                user.passwordpinallowed = 1
                db.session.add(user)
                db.session.commit()

                flash("Account Confirmed.", category="danger")
                return redirect(url_for('auth.changepin'))
            else:
                flash("Incorrect Seed Entry", category="danger")
                return redirect(url_for('auth.retrievepin'))

    return render_template('/auth/security/lostpinsubmit.html',
                           form=form
                           )


@auth.route('/change-pin', methods=['GET', 'POST'])
@website_offline
def changepin():
    form = ChangePinForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(id=current_user.id).first()
            cryptedpwd = User.cryptpassword(password=form.newpin2.data)
            user.wallet_pin = cryptedpwd
            user.passwordpinallowed = 0
            db.session.add(user)
            db.session.commit()
            flash('Your pin has been updated!', category="success")
            return redirect(url_for('index'))
        else:
            flash('Invalid form.  Pin must be 4 digits and match!',
                  category="danger")
            return redirect(url_for('auth.changepin'))
    return render_template('/auth/security/resetpin.html',
                           form=form
                           )


@auth.route('/deleteaccount', methods=['GET', 'POST'])
@website_offline
def deleteaccount():

    title = "DELETE ACCOUNT"
    form = Deleteaccountform()
    # get the user
    user = db.session.query(User).filter_by(id=current_user.id).first()
    # get his wallets
    # get btc wallet
    # get btccash wallet
    userbtccash = db.session.query(BchWallet) \
        .filter(user.id == BchWallet.user_id).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            if userbtccash.currentbalance > 0:
                flash("Cannot Delete Account with BCH coins in the wallet.",
                      category="danger")
                return redirect(url_for('auth.deleteaccount'))
            else:
                # query everything related to user first

                # get the seed
                userseed = db.session.query(AccountSeedWords) \
                    .filter(user.id == AccountSeedWords.user_id).first()
                # get user stats
                userstats = db.session.query(StatisticsUser) \
                    .filter(user.id == StatisticsUser.user_id).first()
                # get achievements
                userachs = db.session.query(whichAch) \
                    .filter(user.id == whichAch.user_id).first()
                # get exp
                userexp = db.session.query(UserAchievements) \
                    .filter(user.id == UserAchievements.user_id).first()
                # get browser history
                userbrowser = db.session.query(userHistory) \
                    .filter(user.id == userHistory.user_id).first()
                # get shopping cart total
                usercarttotal = db.session.query(ShoppingCartTotal) \
                    .filter(user.id == ShoppingCartTotal.customer).first()
                # get shopping cart total
                usercart = db.session.query(ShoppingCart) \
                    .filter(user.id == ShoppingCart.customer_id).first()
                if usercart is None:
                    usercartfound = 0
                else:
                    usercartfound = 1

                # get btccash wallet
                userbtccash = db.session.query(BchWallet) \
                    .filter(user.id == BchWallet.user_id).first()
                # get user fees
                userfees = db.session.query(UserFees) \
                    .filter(user.id == AccountSeedWords.user_id).first()

                # see if seed matches the account
                w00 = form.seedanswer0.data
                w01 = form.seedanswer1.data
                w02 = form.seedanswer2.data
                w03 = form.seedanswer3.data
                w04 = form.seedanswer4.data
                w05 = form.seedanswer5.data

                if w00 == userseed.word00 and \
                        w01 == userseed.word01 and \
                        w02 == userseed.word02 and \
                        w03 == userseed.word03 and \
                        w04 == userseed.word04 and \
                        w05 == userseed.word05:

                    # delete the user
                    db.session.delete(user)
                    # delete the seed
                    db.session.delete(userseed)
                    # delete user stats
                    db.session.delete(userstats)
                    # delete achievements
                    db.session.delete(userachs)
                    # delete exp
                    db.session.delete(userexp)
                    # delete browser history
                    db.session.delete(userbrowser)
                    # delete shopping cart
                    if usercartfound == 1:
                        db.session.delete(usercart)
                    # delete shopping cart total
                    db.session.delete(usercarttotal)
                    # delete btccash wallet
                    db.session.delete(userbtccash)
                    # delete user fees
                    db.session.delete(userfees)

                    # logout user
                    current_user.is_authenticated = False
                    logout_user()
                    # commit
                    db.session.commit()
                    flash("Account Deleted."
                          "  Thank you for using Clearnet Market.", category="danger")
                    return redirect(url_for('index'))
                else:
                    flash("Incorrect Seed Entry", category="danger")
                    return redirect(url_for('index'))
        else:
            flash('Invalid form.  Seed doesnt match', category="danger")
            return redirect(url_for('auth.changepin'))

    return render_template('/auth/security/deleteaccount.html',
                           form=form,
                           user=user,
                           title=title
                           )
