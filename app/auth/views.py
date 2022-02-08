from app.auth import auth
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user, login_user
from app import db, UPLOADED_FILES_DEST
from app.auth.profile_image_resizer import imagespider
import os
from datetime import datetime
from sqlalchemy.orm.exc import UnmappedInstanceError
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
from app.common.functions import id_generator_picture1
from app.achs.v import becamevendor
from app.achs.a import newbie

from app.classes.vendor import \
    vendorVerification
from app.classes.userdata import \
    userHistory
from app.classes.models import WordSeeds
from app.classes.profile import \
    StatisticsUser, \
    StatisticsVendor
from app.classes.item import \
    ShoppingCartTotal, \
    ShoppingCart
from app.classes.achievements import \
    UserAchievements, \
    whichAch
from app.classes.auth import \
    User, \
    UserFees, \
    AccountSeedWords
from app.auth.forms import LoginForm, \
    RegistrationForm, \
    CheckSeed, \
    ChangePasswordForm, \
    myaccount_form_factory, \
    VacationForm, \
    vendorSignup, \
    ConfirmSeed, \
    ChangePinForm, \
    Deleteaccountform
from app.classes.wallet_bch import \
    BchWallet
from app.common.decorators import \
    ping_user, \
    website_offline, \
    login_required
from app.wallet_bch.wallet_btccash_work import \
    btc_cash_create_wallet
from app.common.functions import mkdir_p, userimagelocation



# btc cash work

# forms
# models


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

            get_words = db.session.query(
                WordSeeds).order_by(func.random()).limit(6)
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
    return render_template('auth/account/myaccount.html',
                           title=title,
                           form=form,
                           now=now,
                           user=user,
                           vacform=vacform)


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
                    return redirect(url_for('vendorverification.vendorverificationhome'))
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
