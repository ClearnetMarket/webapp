from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user, login_user
from app.auth import auth
from app import db, UPLOADED_FILES_DEST_USER
import os
from datetime import datetime
from sqlalchemy.orm.exc import UnmappedInstanceError
from werkzeug.datastructures import CombinedMultiDict
from sqlalchemy.sql import func
from app.common.functions import mkdir_p, userimagelocation
from app.achs.v import becamevendor
from app.achs.a import newbie
from app.classes.vendor import \
    Vendor_VendorVerification
from app.classes.userdata import \
    User_DataHistory
from app.classes.models import Query_CategoryCats
from app.classes.profile import \
    Profile_StatisticsUser, \
    Profile_StatisticsVendor
from app.classes.item import \
    Item_ShoppingCartTotal, \
    Item_CheckoutShoppingCart
from app.classes.achievements import \
    Achievements_UserAchievements, \
    Achievements_WhichAch
from app.classes.auth import \
    Auth_User, \
    Auth_UserFees, \
    Auth_AccountSeedWords
from app.auth.forms import LoginForm, \
    RegistrationForm, \
    CheckSeed, \
    ChangePasswordForm, \
    myaccount_form_factory, \
    VacationForm, \
    vendorSignup, \
    confirm_seed, \
    ChangePinForm, \
    Deleteaccountform
from app.classes.wallet_bch import \
    Bch_Wallet
from app.common.decorators import \
    website_offline, \
    login_required
from app.wallet_bch.wallet_btccash_work import \
    btc_cash_create_wallet
from app.auth.profile_images.profile_images import \
    deleteprofileimage, \
    image1


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
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session\
                .query(Auth_User)\
                .filter_by(username=form.username.data)\
                .first()
            if user:
                if user.confirmed == 1:
                    if user is not None:
                        if Auth_User.decryptpassword(pwdhash=user.password_hash, password=form.password_hash.data):
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
                    return redirect(url_for('auth.confirm_seed'))
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
        cryptedpwd = Auth_User.cryptpassword(password=form.password.data)
        cryptedpin = Auth_User.cryptpassword(password=form.walletpin.data)
        namefull = form.country.data
        name = namefull.numericcode
        currencyfull = form.currency.data
        cur = currencyfull.code

        # add user to db
        new_user = Auth_User(
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
        stats = Profile_StatisticsUser(
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
        achselect = Achievements_WhichAch(
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
        ach = Achievements_UserAchievements(
            user_id=new_user.id,
            username=new_user.username,
            experiencepoints=0,
            level=1,
        )

        # create browser history
        browserhistory = User_DataHistory(
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

        # create checkout_shopping_cart for user
        newcart = Item_ShoppingCartTotal(
            customer=new_user.id,
            btc_cash_sumofitem=0,
            btc_cash_price=0,
            shipping_btc_cashprice=0,
            total_btc_cash_price=0,
            percent_off_order=0,
            btc_cash_off=0,
        )

        setfees = Auth_UserFees(user_id=new_user.id,
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

        # achievement
        newbie(user_id=new_user.id)

        # make a user a directory

        getuserlocation = userimagelocation(user_id=new_user.id)
        userfolderlocation = os.path.join(UPLOADED_FILES_DEST_USER,
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
        return redirect(url_for('auth.create_account_seed'))

    return render_template('/auth/register.html', form=form)


@auth.route('/accountseed', methods=["GET"])
@login_required
def create_account_seed():

    # get the current user
    user = db.session.query(Auth_User).filter_by(id=current_user.id).first()

    # see if user seed created..
    userseed = db.session \
        .query(Auth_AccountSeedWords) \
        .filter(user.id == Auth_AccountSeedWords.user_id) \
        .first()

    if request.method == 'GET':
        if userseed is None:
            # created the wallet seed
            word_list = []

            get_words = db.session.query(
                Query_CategoryCats).order_by(func.random()).limit(6)
            for f in get_words:
                word_list.append(f.text)
                print(f.text)
            word00 = str(word_list[0]).lower()
            word01 = str(word_list[1]).lower()
            word02 = str(word_list[2]).lower()
            word03 = str(word_list[3]).lower()
            word04 = str(word_list[4]).lower()
            word05 = str(word_list[5]).lower()

            addseedtodb = Auth_AccountSeedWords(user_id=user.id,
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
def confirm_seed():

    form = confirm_seed()

    # get the user
    user = db.session\
        .query(Auth_User)\
        .filter(current_user.id == Auth_User.id)\
        .first()

    if user.confirmed == 1:
        flash("You have already been confirmed", category="danger")
        return redirect(url_for('index'))
    if request.method == 'POST':
        # get the users seed
        userseed = db.session.query(Auth_AccountSeedWords) \
            .filter(user.id == Auth_AccountSeedWords.user_id)\
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
            return redirect(url_for('auth.confirm_seed'))

    if request.method == 'GET':
        return render_template('/auth/confirm_seed.html', form=form)


@auth.route('/my-account/', methods=['GET', 'POST'])
@website_offline
@login_required
def my_account():
    now = datetime.utcnow()
    title = 'My Account'

    user = db.session\
        .query(Auth_User)\
        .filter_by(username=current_user.username)\
        .first()

    vacform = VacationForm()
    myaccountform = myaccount_form_factory(user)

    form = myaccountform(
        CombinedMultiDict((request.files, request.form)),
        Bio=user.bio,
        country=user.country,
    )

    if request.method == 'POST':

        if vacform.Vacation.data:
            return redirect(url_for('vendorcreate.vendorcreate_vacation', username=current_user.username))

        if form.delete.data:
            # type 1 = make database have user-unknown
            deleteprofileimage(id=user.id, img=user.profileimage, type=1)
            # deleted profile image
            return redirect(url_for('auth.my_account', username=current_user.username))

        if form.submit.data and form.validate_on_submit():
            # gets user location on server
            if form.imageprofile.data:
                userlocation = os.path.join(
                    UPLOADED_FILES_DEST_USER, str(user.usernode), (str(user.id)))
                image1(formdata=form.imageprofile.data,
                       directoryifitemlisting=userlocation, user=user)
            # dropdown changes on forms
            origin_countryfull = form.origin_country_1.data
            origin_country = origin_countryfull.numericcode
            currencyfull = form.currency1.data
            cur = currencyfull.code
            user.currency = cur,
            user.bio = form.Bio.data,
            user.country = origin_country,
            db.session.add(user)
            db.session.commit()
            flash("Information Updated", category="success")
            return redirect(url_for('auth.my_account', username=current_user.username))
        else:
            flash("Form Error", category="danger")
            return redirect(url_for('auth.my_account', username=current_user.username))
    return render_template('auth/account/myaccount.html',
                           title=title,
                           form=form,
                           now=now,
                           user=user,
                           vacform=vacform)


@auth.route('/vendor-signup', methods=['GET', 'POST'])
@website_offline
@login_required
def setup_account():
    now = datetime.utcnow()
    form = vendorSignup(request.form)
    user = db.session \
        .query(Auth_User) \
        .filter(Auth_User.id == current_user.id) \
        .first()

    if request.method == 'POST':
        if form.validate_on_submit():
            if user.username == form.username.data:
                if form.agreement.data is True:

                    user.vendor_account = 1,
                    user.sellingfrom = form.country.data

                    stats = Profile_StatisticsVendor(
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

                    addverify = Vendor_VendorVerification(
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
                    return redirect(url_for('vendorverification.vendorverification_home'))
                else:
                    flash("Please accept the agreement", category="danger")
                    return redirect(url_for('auth.setup_account'))
            else:
                flash("invalid username", category="danger")
                return redirect(url_for('auth.setup_account'))
        else:
            flash(form.errors, category="danger")
            return redirect(url_for('auth.setup_account'))

    return render_template('/auth/account/setup_account.html', form=form)


@auth.route('/lost-password', methods=['GET', 'POST'])
def retrieve_password():

    form = CheckSeed()
    if request.method == 'POST':
        if form.validate_on_submit():
            # get the user based off of form
            user = db.session.query(Auth_User).filter_by(
                username=form.username.data).first()
            # match the seed to the user
            userseed = db.session.query(Auth_AccountSeedWords) \
                .filter(user.id == Auth_AccountSeedWords.user_id).first()

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
                return redirect(url_for('auth.change_password'))
            else:
                flash("Incorrect Seed Entry", category="danger")
                return redirect(url_for('auth.retrieve_password'))

    return render_template('/auth/security/lostPassword.html',
                           form=form
                           )


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():

    form = ChangePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Auth_User.query.filter_by(id=current_user.id).first()
            user = Auth_User.query.filter_by(id=current_user.id).first()
            cryptedpwd = Auth_User.cryptpassword(
                password=form.newpasswordtwo.data)

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
def retrieve_pin():
    form = CheckSeed()
    if request.method == 'POST':
        if form.validate_on_submit():
            # get the user based off of form
            user = db.session.query(Auth_User).filter_by(
                username=form.username.data).first()
            # match the seed to the user
            userseed = db.session.query(Auth_AccountSeedWords) \
                .filter(user.id == Auth_AccountSeedWords.user_id).first()

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
                return redirect(url_for('auth.change_pin'))
            else:
                flash("Incorrect Seed Entry", category="danger")
                return redirect(url_for('auth.retrieve_pin'))

    return render_template('/auth/security/lostpinsubmit.html',
                           form=form
                           )


@auth.route('/change-pin', methods=['GET', 'POST'])
@website_offline
def change_pin():
    form = ChangePinForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Auth_User.query.filter_by(id=current_user.id).first()
            cryptedpwd = Auth_User.cryptpassword(password=form.newpin2.data)
            user.wallet_pin = cryptedpwd
            user.passwordpinallowed = 0
            db.session.add(user)
            db.session.commit()
            flash('Your pin has been updated!', category="success")
            return redirect(url_for('index'))
        else:
            flash('Invalid form.  Pin must be 4 digits and match!',
                  category="danger")
            return redirect(url_for('auth.change_pin'))
    return render_template('/auth/security/resetpin.html',
                           form=form
                           )


@auth.route('/delete_account', methods=['GET', 'POST'])
@website_offline
def delete_account():

    title = "DELETE ACCOUNT"
    form = Deleteaccountform()
    # get the user
    user = db.session.query(Auth_User).filter_by(id=current_user.id).first()
    # get his wallets
    # get btc wallet
    # get btccash wallet
    userbtccash = db.session.query(Bch_Wallet) \
        .filter(user.id == Bch_Wallet.user_id).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            if userbtccash.currentbalance > 0:
                flash("Cannot Delete Account with BCH coins in the wallet.",
                      category="danger")
                return redirect(url_for('auth.delete_account'))
            else:
                # query everything related to user first

                # get the seed
                userseed = db.session.query(Auth_AccountSeedWords) \
                    .filter(user.id == Auth_AccountSeedWords.user_id).first()
                # get user stats
                userstats = db.session.query(Profile_StatisticsUser) \
                    .filter(user.id == Profile_StatisticsUser.user_id).first()
                # get achievements
                userachs = db.session.query(Achievements_WhichAch) \
                    .filter(user.id == Achievements_WhichAch.user_id).first()
                # get exp
                userexp = db.session.query(Achievements_UserAchievements) \
                    .filter(user.id == Achievements_UserAchievements.user_id).first()
                # get browser history
                userbrowser = db.session.query(User_DataHistory) \
                    .filter(user.id == User_DataHistory.user_id).first()
                # get shopping cart total
                usercarttotal = db.session.query(Item_ShoppingCartTotal) \
                    .filter(user.id == Item_ShoppingCartTotal.customer).first()
                # get shopping cart total
                usercart = db.session.query(Item_CheckoutShoppingCart) \
                    .filter(user.id == Item_CheckoutShoppingCart.customer_id).first()
                if usercart is None:
                    usercartfound = 0
                else:
                    usercartfound = 1

                # get btccash wallet
                userbtccash = db.session.query(Bch_Wallet) \
                    .filter(user.id == Bch_Wallet.user_id).first()
                # get user fees
                userfees = db.session.query(Auth_UserFees) \
                    .filter(user.id == Auth_AccountSeedWords.user_id).first()

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
            return redirect(url_for('auth.change_pin'))

    return render_template('/auth/security/delete_account.html',
                           form=form,
                           user=user,
                           title=title
                           )
