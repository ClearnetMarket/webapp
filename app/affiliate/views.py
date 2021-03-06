from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.affiliate import affiliate
from app import db

from datetime import datetime
# forms
from app.affiliate.forms import \
    AffiliateSignup, \
    AffiliateCode

# models
from app.classes.affiliate import Affiliate_Orders
from app.classes.auth import Auth_User

from app.classes.affiliate import Affiliate_Overview, \
    Affiliate_Stats, \
    Affiliate_Id

from app.common.decorators import \
    website_offline, \
    login_required


@affiliate.route('/overview', methods=['GET'])
@website_offline
def aff_overview():
    return render_template('/affiliate/overview.html')


@affiliate.route('/signup', methods=['GET', 'POST'])
@login_required
@website_offline
def aff_become_aff():
    now = datetime.utcnow()
    vendorsignupForm = AffiliateSignup()
    user = db.session.query(Auth_User).filter_by(
        username=current_user.username).first()

    if request.method == 'POST':

        if vendorsignupForm.validate_on_submit():
            if user.username == vendorsignupForm.username.data:
                if vendorsignupForm.agreement.data is True:

                    affaccount_overview = Affiliate_Overview(
                        user_id=user.id,
                        buyerdiscount=2.5,
                        buyerdiscount_time=now,
                        aff_fee=2.5,
                        aff_fee_time=now,
                        aff_link_1='',
                        aff_link_2='',
                    )

                    affaccount_stats = Affiliate_Stats(
                        user_id=user.id,
                        promocode='',
                        totalitemsordered=0,
                        promoenteredcount=0,
                        btc_earned=0,
                        btc_cash_earned=0,

                    )
                    db.session.add(affaccount_stats)
                    db.session.add(affaccount_overview)
                    db.session.commit()

                    user.affiliate_account = affaccount_overview.user_id
                    db.session.add(user)
                    db.session.commit()

                    flash("Welcome as a protos Affiliate",
                          category="success")
                    return redirect(url_for('affiliate.aff_home'))
                else:
                    flash("Please accept the agreement", category="danger")
                    return redirect(url_for('affiliate.aff_become_aff'))
            else:
                flash("invalid username", category="danger")
                return redirect(url_for('affiliate.aff_become_aff'))
        else:
            flash(vendorsignupForm.errors, category="danger")
            return redirect(url_for('affiliate.aff_become_aff'))

    return render_template('/affiliate/homecontent/becomeaff.html',
                           vendorsignupForm=vendorsignupForm)


@affiliate.route('/home', methods=['GET', 'POST'])
@login_required
@website_offline
def aff_home():
    now = datetime.utcnow()
    promocodeform = AffiliateCode()

    # users promo overview
    userpromooverview = db.session.query(
        Affiliate_Overview).filter_by(user_id=current_user.id).first()
    # users promo stats
    userpromostats = db.session.query(Affiliate_Stats).filter_by(
        user_id=current_user.id).first()
    # users promo code

    userpromocode = db.session.query(Affiliate_Id).filter_by(
        user_id=current_user.id).first()
    if userpromocode is not None:
        # get last 20 affiliates orders..
        latest_affiliates = db.session.query(Affiliate_Orders).filter(
            Affiliate_Orders.affiliate_code == userpromocode.promocode).order_by(Affiliate_Orders.id.desc()).limit(20)
    else:
        latest_affiliates = None

    if request.method == 'POST':
        if promocodeform.submit.data:
            if promocodeform.validate_on_submit():
                if userpromocode is None:
                    seeifpromoexists = db.session.query(Affiliate_Id).filter_by(
                        promocode=promocodeform.thecode.data).first()
                    if seeifpromoexists is None:
                        newpromocode = Affiliate_Id(
                            user_id=current_user.id,
                            promocode=promocodeform.thecode.data)

                        userpromooverview.promocode = promocodeform.thecode.data
                        userpromostats.promocode = promocodeform.thecode.data

                        db.session.add(userpromooverview)
                        db.session.add(newpromocode)
                        db.session.commit()
                        flash("Success creating promo code", category="success")
                        return redirect(url_for('affiliate.aff_home'))
                    else:
                        flash("Code exists, try another..", category="danger")
                        return redirect(url_for('affiliate.aff_home'))
                else:
                    flash("Cant create code, you already have one",
                          category="danger")
                    return redirect(url_for('affiliate.aff_home'))
            else:
                flash(
                    "Form error.  5-15 characters.  No special characters.", category="danger")
                return redirect(url_for('affiliate.aff_home'))

    return render_template('/affiliate/home.html',
                           now=now,
                           userpromooverview=userpromooverview,
                           promocodeform=promocodeform,
                           userpromocode=userpromocode,
                           userpromostats=userpromostats,
                           latest_affiliates=latest_affiliates,
                           )


@affiliate.route('/images', methods=['GET', 'POST'])
@login_required
@website_offline
def aff_images():
    now = datetime.utcnow()

    return render_template('/affiliate/affimages.html',
                           now=now,
                           )
