from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.vendorverification import vendorverification
from decimal import Decimal
from app.achs.v import obtainedtrustlevel
from app.common.decorators import \
    website_offline, \
    login_required, \
    ping_user, \
    vendoraccount_required
from app.common.functions import btc_cash_convertlocaltobtc
# forms
from app.vendorverification.forms import \
    vendorVerify, \
    ConfirmCancel

from app.wallet_bch.wallet_btccash_work import \
    btc_cash_sendCoinfromHoldings,\
    btc_cash_sendCointoHoldings

# models
from app.classes.achievements import UserAchievements
from app.classes.auth import User
from app.classes.vendor import \
    Orders, \
    vendorVerification
from app.classes.wallet_bch import *
# End Models


@vendorverification.route('/becomeverified', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorverificationhome():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()

    seeifvendoropenorder = db.session\
        .query(Orders)\
        .filter(Orders.released == 0, Orders.completed == 0)\
        .first()

    if seeifvendoropenorder is None:
        allow = 1
    else:
        allow = 0
    hundred = btc_cash_convertlocaltobtc(amount=100, currency=0)
    twofity = btc_cash_convertlocaltobtc(amount=250, currency=0)
    fivehundred = btc_cash_convertlocaltobtc(amount=500, currency=0)
    thousand = btc_cash_convertlocaltobtc(amount=1000, currency=0)
    twentyfivehundred = btc_cash_convertlocaltobtc(amount=2500, currency=0)

    if request.method == 'POST':
        if form.cancel.data:
            if allow == 1:

                return redirect(url_for('vendorverification.vendorverificationcancel'))
            else:
                flash("Cannot Cancel yur verification", category="danger")
        if getverify.vendor_level == 0:
            if form.levelzero.data:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendorcreate.tradeOptions'))
            elif form.levelone.data:
                return redirect(url_for('vendorverification.vendorverification_confirm_level1'))
            elif form.leveltwo.data:
                return redirect(url_for('vendorverification.vendorverification_confirm_level2'))
            elif form.levelthree.data:
                return redirect(url_for('vendorverification.vendorverification_confirm_level3'))
            elif form.levelfour.data:
                return redirect(url_for('vendorverification.vendorverification_confirm_level4'))
            elif form.levelfive.data:
                return redirect(url_for('vendorverification.vendorverification_confirm_level5'))
            else:
                pass
        else:
            return redirect(url_for('vendor.upgradevendorverification'))

    return render_template('/vendor/verification/verification.html',
                           form=form,
                           user=user,
                           allow=allow,
                           getverify=getverify,
                           now=now,
                           hundred=hundred,
                           twofity=twofity,
                           fivehundred=fivehundred,
                           thousand=thousand,
                           twentyfivehundred=twentyfivehundred,
                           )


@vendorverification.route('/cancelverified', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorverificationcancel():
    now = datetime.utcnow()
    form = ConfirmCancel()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()
    user1getlevel = db.session\
        .query(UserAchievements)\
        .filter_by(username=user.username)\
        .first()
    user1pictureid = str(user1getlevel.level)
    seeifvendoropenorder = db.session\
        .query(Orders)\
        .filter(Orders.released == 0, Orders.completed == 0)\
        .first()
    if seeifvendoropenorder is None:
        allow = 1
    else:
        allow = 0
    hundred = btc_cash_convertlocaltobtc(amount=100, currency=0)
    twofity = btc_cash_convertlocaltobtc(amount=250, currency=0)
    fivehundred = btc_cash_convertlocaltobtc(amount=500, currency=0)
    thousand = btc_cash_convertlocaltobtc(amount=1000, currency=0)
    twentyfivehundred = btc_cash_convertlocaltobtc(amount=2500, currency=0)

    if request.method == 'POST':
        if getverify.vendor_level != 0:
            if form.confirmcancel.data:
                if allow == 1:
                    btc_cash_sendCoinfromHoldings(amount=getverify.amount,
                                                  user_id=getverify.vendor_id,
                                                  comment=getverify.vendor_level
                                                  )
                    getverify.vendor_level = 0
                    getverify.timestamp = now
                    getverify.amount = 0
                    db.session.add(getverify)
                    db.session.commit()

                    flash("Trust level removed, account refunded",
                          category="success")
                    return redirect(url_for('vendorcreate.tradeOptions'))
                else:
                    flash("Cannot Cancel yur verification", category="danger")
                    return redirect(url_for('vendorverification.vendorverificationhome'))
            else:
                return redirect(url_for('vendorverification.vendorverificationhome'))
        else:
            return redirect(url_for('vendorverification.vendorverificationhome'))

    return render_template('/vendor/verification/confirmcancel.html',
                           form=form,
                           user=user,
                           allow=allow,
                           getverify=getverify,
                           now=now,
                           hundred=hundred,
                           twofity=twofity,
                           fivehundred=fivehundred,
                           thousand=thousand,
                           twentyfivehundred=twentyfivehundred,
                           user1pictureid=user1pictureid
                           )


@vendorverification.route('/becomeverified-level1', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorverification_confirm_level1():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()

    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        hundred = btc_cash_convertlocaltobtc(amount=100, currency=0)
        Decimalhundred = Decimal(hundred)

        if request.method == 'POST':
            if form.levelone.data:
                # 100 dollars
                if useramount > Decimalhundred:
                    btc_cash_sendCointoHoldings(
                        amount=hundred, user_id=current_user.id, comment=1)
                    getverify.vendor_level = 1
                    getverify.timestamp = now
                    getverify.amount = Decimalhundred
                    db.session.add(getverify)

                    obtainedtrustlevel(user_id=user.id)

                    db.session.commit()
                    flash("You are now a trust level 1 vendor. "
                          "The BTC has been deducted from your account", category="success")
                    return redirect(url_for('vendorcreate.tradeOptions'))
                else:
                    # user doesnt have 100$
                    flash(
                        "You do not have enough bitcoin in your wallet_btc.", category="danger")
                    return redirect(url_for('vendorverification.vendorverificationhome'))
            else:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendorcreate.tradeOptions'))

        return render_template('/vendor/verification/confirmverification_level1.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               hundred=hundred,
                               )
    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendorverification.route('/becomeverified-level2', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorverification_confirm_level2():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()
    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()

        useramount = userwallet.currentbalance

        twofity = btc_cash_convertlocaltobtc(amount=250, currency=0)
        Decimaltwofity = Decimal(twofity)

        if request.method == 'POST':
            if form.leveltwo.data:
                if useramount > Decimaltwofity:
                    # 250 dollars
                    btc_cash_sendCointoHoldings(
                        amount=twofity, user_id=current_user.id, comment=2)
                    getverify.vendor_level = 2
                    getverify.timestamp = now
                    getverify.amount = Decimaltwofity
                    db.session.add(getverify)

                    obtainedtrustlevel(user_id=user.id)

                    db.session.commit()
                    flash("You are now a trust level 2 vendor. "
                          "The BTC has been deducted from your account", category="success")
                    return redirect(url_for('vendorcreate.tradeOptions'))
                else:
                    # user doesnt have 250$
                    flash(
                        "You do not have enough bitcoin in your wallet_btc.", category="danger")
                    return redirect(url_for('vendorverification.vendorverificationhome'))
            else:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendorcreate.tradeOptions'))

        return render_template('/vendor/verification/confirmverification_level2.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               twofity=twofity,
                               )
    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendorverification.route('/becomeverified-level3', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorverification_confirm_level3():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()

    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        fivehundred = btc_cash_convertlocaltobtc(amount=500, currency=0)
        Decimalfivehundred = Decimal(fivehundred)

        if request.method == 'POST':
            if form.levelthree.data:
                if useramount > Decimalfivehundred:
                    btc_cash_sendCointoHoldings(
                        amount=fivehundred, user_id=current_user.id, comment=3)
                    getverify.vendor_level = 3
                    getverify.timestamp = now
                    getverify.amount = Decimalfivehundred
                    db.session.add(getverify)

                    obtainedtrustlevel(user_id=user.id)

                    db.session.commit()
                    flash("You are now a trust level 3 vendor. "
                          "The BTC has been deducted from your account",
                          category="success")
                    return redirect(url_for('vendorcreate.tradeOptions'))
                else:
                    # user doesnt have 500$
                    flash(
                        "You do not have enough bitcoin in your wallet_btc.", category="danger")
                    return redirect(url_for('vendorverification.vendorverificationhome'))
            else:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendorcreate.tradeOptions'))

        return render_template('/vendor/verification/confirmverification_level3.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               fivehundred=fivehundred,
                               )
    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendorverification.route('/becomeverified-level4', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorverification_confirm_level4():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()
    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        thousand = btc_cash_convertlocaltobtc(amount=1000, currency=0)
        Decimalthousand = Decimal(thousand)

        if request.method == 'POST':
            if useramount > Decimalthousand:
                btc_cash_sendCointoHoldings(
                    amount=thousand, user_id=current_user.id, comment=4)
                getverify.vendor_level = 4
                getverify.timestamp = now
                getverify.amount = Decimalthousand
                db.session.add(getverify)

                obtainedtrustlevel(user_id=user.id)

                db.session.commit()
                flash("You are now a trust level 4 vendor."
                      " The BTC has been deducted from your account",
                      category="success")
                return redirect(url_for('vendorcreate.tradeOptions'))
            else:
                # user doesnt have 1000$
                flash("You do not have enough bitcoin in your wallet_btc.",
                      category="danger")
                return redirect(url_for('vendorverification.vendorverificationhome'))

        return render_template('/vendor/verification/confirmverification_level4.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               thousand=thousand,
                               )
    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendorverification.route('/becomeverified-level5', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorverification_confirm_level5():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()
    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        twentyfivehundred = btc_cash_convertlocaltobtc(amount=2500, currency=0)
        Decimaltwentyfivehundred = Decimal(twentyfivehundred)

        if request.method == 'POST':
            if form.levelfive.data:
                if useramount > Decimaltwentyfivehundred:
                    btc_cash_sendCointoHoldings(
                        amount=twentyfivehundred, user_id=current_user.id, comment=5)
                    getverify.vendor_level = 5
                    getverify.timestamp = now
                    getverify.amount = Decimaltwentyfivehundred
                    db.session.add(getverify)

                    obtainedtrustlevel(user_id=user.id)

                    db.session.commit()
                    flash("You are now a trust level 5 vendor. "
                          "The BTC has been deducted from your account",
                          category="success")
                    return redirect(url_for('vendorcreate.tradeOptions'))
                else:
                    # user doesnt have 2500$
                    flash(
                        "You do not have enough bitcoin in your wallet_btc.", category="danger")
                    return redirect(url_for('vendorverification.vendorverificationhome'))
            else:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendorcreate.tradeOptions'))

        return render_template('/vendor/verification/confirmverification_level5.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               twentyfivehundred=twentyfivehundred,
                               )

    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendorverification.route('/upgradeverified', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def upgradevendorverification():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()

    userwallet = db.session\
        .query(BchWallet)\
        .filter_by(user_id=current_user.id)\
        .first()
    useramount = userwallet.currentbalance

    twofity = btc_cash_convertlocaltobtc(amount=250, currency=0)
    fivehundred = btc_cash_convertlocaltobtc(amount=500, currency=0)
    thousand = btc_cash_convertlocaltobtc(amount=1000, currency=0)
    twentyfivehundred = btc_cash_convertlocaltobtc(amount=2500, currency=0)

    Decimaltwofity = Decimal(twofity)
    Decimalfivehundred = Decimal(fivehundred)
    Decimalthousand = Decimal(thousand)
    Decimaltwentyfivehundred = Decimal(twentyfivehundred)

    if request.method == 'POST':
        if current_user.id == getverify.vendor_id:
            # return refund
            # get new badge
            if form.leveltwo.data:
                if getverify.vendor_level == 1:
                    if useramount > Decimaltwofity:
                        btc_cash_sendCoinfromHoldings(
                            amount=getverify.amount, user_id=getverify.vendor_id, comment=getverify.vendor_level)
                        btc_cash_sendCointoHoldings(
                            amount=twofity, user_id=current_user.id, comment=2)
                        getverify.vendor_level = 2
                        getverify.timestamp = now
                        getverify.amount = Decimaltwofity
                        db.session.add(getverify)

                        db.session.commit()

                        flash("You are now a trust level 2 vendor. "
                              "The BTC has been deducted from your account",
                              category="success")
                        return redirect(url_for('vendorcreate.tradeOptions'))
                    else:
                        # user doesnt have 250$
                        flash(
                            "You do not have enough bitcoin in your wallet_btc.", category="danger")
                        return redirect(url_for('vendorverification.vendorverificationhome'))

            elif form.levelthree.data:
                if getverify.vendor_level == 1 \
                        or getverify.vendor_level == 2:
                    if useramount > Decimalfivehundred:
                        btc_cash_sendCoinfromHoldings(amount=getverify.amount, user_id=getverify.vendor_id,
                                                      comment=getverify.vendor_level)
                        btc_cash_sendCointoHoldings(
                            amount=fivehundred, user_id=current_user.id, comment=3)
                        getverify.vendor_level = 3
                        getverify.timestamp = now
                        getverify.amount = Decimalfivehundred
                        db.session.add(getverify)

                        db.session.commit()

                        flash("You are now a trust level 3 vendor. "
                              "The BTC has been deducted from your account",
                              category="success")
                        return redirect(url_for('vendorcreate.tradeOptions'))
                    else:
                        # user doesnt have 500$
                        flash(
                            "You do not have enough bitcoin in your wallet_btc.", category="danger")
                        return redirect(url_for('vendorverification.vendorverificationhome'))

            elif form.levelfour.data:
                if getverify.vendor_level == 1 \
                        or getverify.vendor_level == 2 \
                        or getverify.vendor_level == 3:
                    if useramount > Decimalthousand:
                        btc_cash_sendCoinfromHoldings(
                            amount=getverify.amount, user_id=getverify.vendor_id, comment=getverify.vendor_level)
                        btc_cash_sendCointoHoldings(
                            amount=thousand, user_id=current_user.id, comment=4)

                        getverify.vendor_level = 4
                        getverify.timestamp = now
                        getverify.amount = Decimalthousand
                        db.session.add(getverify)
                        db.session.commit()

                        flash("You are now a trust level 4 vendor."
                              " The BTC has been deducted from your account",
                              category="success")
                        return redirect(url_for('vendorcreate.tradeOptions'))
                    else:
                        # user doesnt have 1000$
                        flash(
                            "You do not have enough bitcoin in your wallet_btc.", category="danger")
                        return redirect(url_for('vendorverification.vendorverificationhome'))
            elif form.levelfive.data:
                if getverify.vendor_level == 1 \
                        or getverify.vendor_level == 2 \
                        or getverify.vendor_level == 3 \
                        or getverify.vendor_level == 4:
                    if useramount > Decimaltwentyfivehundred:
                        btc_cash_sendCoinfromHoldings(
                            amount=getverify.amount, user_id=getverify.vendor_id, comment=getverify.vendor_level)
                        btc_cash_sendCointoHoldings(
                            amount=twentyfivehundred, user_id=current_user.id, comment=5)

                        getverify.vendor_level = 5
                        getverify.timestamp = now
                        getverify.amount = Decimaltwentyfivehundred
                        db.session.add(getverify)
                        db.session.commit()

                        flash("You are now a trust level 5 vendor."
                              " The BTC has been deducted from your account",
                              category="success")
                        return redirect(url_for('vendorcreate.tradeOptions'))
                    else:
                        # user doesnt have $
                        flash(
                            "You do not have enough bitcoin in your wallet_btc.", category="danger")
                        return redirect(url_for('vendorverification.vendorverificationhome'))
            else:
                flash("Form Error", category="danger")
                return redirect(url_for('vendorverification.vendorverificationhome'))
        else:
            flash("Form Error", category="danger")
            return redirect(url_for('vendorverification.vendorverificationhome'))
    return render_template('/vendor/verification/upgradeverification.html',
                           form=form,
                           user=user,
                           getverify=getverify,
                           now=now,
                           twofity=twofity,
                           fivehundred=fivehundred,
                           thousand=thousand,
                           twentyfivehundred=twentyfivehundred,
                           )
