from flask import \
    render_template,\
    redirect, \
    url_for, \
    flash, \
    request
from app import db

from app.wallet_bch import\
    wallet_bch
from app.wallet_bch.wallet_btccash_work import\
    btc_cash_sendCoin

# models
from app.classes.auth import \
    User

from app.classes.wallet_bch import \
    TransactionsBch,\
    BchWallet,\
    BchWalletFee

# end models
from app.wallet_bch.forms import\
    walletSendcoin
from datetime import \
    datetime
from app.common.functions import\
    floating_decimals
from app.common.decorators import\
    website_offline,\
    ping_user,\
    login_required

from app.achs.b import\
    likemoneyinthebank,\
    withdrawl
from flask_login import\
    current_user,\
    logout_user
from flask_paginate import\
    Pagination,\
    get_page_args
from decimal import\
    Decimal
from app.profile.profilebar import\
    profilebar


@wallet_bch.route('/', methods=['GET', 'POST'])
@website_offline
@login_required
def home():
    now = datetime.utcnow()
    title = "Overview"

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
        user2 = profilebar(user_id1=current_user.id, user_id2=0)

    # pagination
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()
    # PEr Page tells how many search results pages
    inner_window = 1  # search bar at bottom used for .. lots of pages
    outer_window = 1  # search bar at bottom used for .. lots of pages
    per_page = 10

    # Get Transaction history
    transactfull = db.session\
        .query(TransactionsBch)\
        .filter(TransactionsBch.user_id == current_user.id)\
        .order_by(TransactionsBch.id.desc())
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

    try:
        wallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        if wallet.currentbalance > 0:
            likemoneyinthebank(user_id=current_user.id)
            db.session.commit()
    except Exception as e:
        print(str(e))
        return redirect(url_for('auth.login', next=request.url))

    return render_template('/wallet/wallet_btccash/home.html',
                           now=now,
                           title=title,
                           transact=transact,
                           wallet=wallet,
                           transactcount=transactcount,
                           pagination=pagination,
                           user1=user1,
                           user1pictureid=user1pictureid,
                           user1stats=user1stats,
                           user1wallet=user1wallet,
                           user1level=user1level,
                           user1width=user1width,
                           user1ach=user1ach,
                           user1vendorstats=user1vendorstats,
                           user2getlevel=user2getlevel,
                           user2pictureid=user2pictureid,
                           user2stats=user2stats,
                           user2wallet=user2wallet,
                           user2level=user2level,
                           user2width=user2width,
                           user2ach=user2ach,
                           user2vendorstats=user2vendorstats,
                           user2=user2,
                           )


@wallet_bch.route('/bch-send', methods=['GET', 'POST'])
@website_offline
@login_required
def send():
    now = datetime.utcnow()
    title = "Send"
    form = walletSendcoin(request.form)

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
        user2 = profilebar(user_id1=current_user.id, user_id2=0)

    # Get wallet_btc
    wallet = db.session\
        .query(BchWallet)\
        .filter_by(user_id=current_user.id)\
        .first()
    # get walletfee
    walletthefee = db.session\
        .query(BchWalletFee)\
        .filter_by(id=1)\
        .first()
    wfee = Decimal(walletthefee.bch)

    if request.method == "POST":

        if form.validate_on_submit() and current_user.dispute == 0:
            if User.decryptpassword(pwdhash=current_user.wallet_pin, password=form.pin.data):
                sendto = form.sendto.data
                comment = form.description.data
                amount = form.amount.data

                # test wallet_btc stuff for security
                walbal = Decimal(wallet.currentbalance)
                amount2withfee = Decimal(amount) + Decimal(wfee)
                # greater than amount with fee
                if floating_decimals(walbal, 8) >= floating_decimals(amount2withfee, 8):
                    # greater than fee
                    if Decimal(amount) > Decimal(wfee):
                        # add to wallet_btc work
                        btc_cash_sendCoin(
                            user_id=current_user.id,
                            sendto=sendto,
                            amount=amount,
                            comment=comment
                        )
                        # achievement
                        withdrawl(user_id=current_user.id)
                        db.session.commit()
                        flash("Bitcoin Sent: " + str(sendto), category="success")
                        return redirect(url_for('wallet_bch.send'))
                    else:
                        flash("Cannot withdraw amount less than wallet_btc fee: " +
                              str(wfee), category="danger")
                        return redirect(url_for('wallet_bch.send'))
                else:
                    flash(
                        "Cannot withdraw more than your balance including fee", category="danger")
                    return redirect(url_for('wallet_bch.send'))
            else:
                flash(
                    "Invalid Pin. Account will be locked with 5 failed attempts.", category="danger")
                x = int(current_user.fails)
                y = x + 1
                current_user.fails = y
                db.session.add(current_user)
                if int(current_user.fails) == 5:
                    current_user.locked = 1
                    db.session.add(current_user)
                    db.session.commit()
                    flash("Account Locked.", category="danger")
                    logout_user()
                    return redirect(url_for('auth.login'))
                else:
                    db.session.commit()
                    return redirect(url_for('wallet_bch.send'))

    return render_template('/wallet/wallet_btccash/send.html',
                           now=now,
                           title=title,
                           form=form,
                           wfee=wfee,
                           wallet=wallet,
                           user1=user1,
                           user1pictureid=user1pictureid,
                           user1stats=user1stats,
                           user1wallet=user1wallet,
                           user1level=user1level,
                           user1width=user1width,
                           user1ach=user1ach,
                           user1vendorstats=user1vendorstats,
                           user2getlevel=user2getlevel,
                           user2pictureid=user2pictureid,
                           user2stats=user2stats,
                           user2wallet=user2wallet,
                           user2level=user2level,
                           user2width=user2width,
                           user2ach=user2ach,
                           user2vendorstats=user2vendorstats,
                           user2=user2,
                           )


@wallet_bch.route('/btccash-receive', methods=['GET', 'POST'])
@website_offline
@login_required
def receive():
    now = datetime.utcnow()
    title = "Receive"

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
        user2 = profilebar(user_id1=current_user.id, user_id2=0)

    wallet = db.session\
        .query(BchWallet)\
        .filter_by(user_id=current_user.id)\
        .first()

    return render_template('/wallet/wallet_btccash/receive.html',
                           now=now,
                           title=title,
                           wallet=wallet,
                           user1=user1,
                           user1pictureid=user1pictureid,
                           user1stats=user1stats,
                           user1wallet=user1wallet,
                           user1level=user1level,
                           user1width=user1width,
                           user1ach=user1ach,
                           user1vendorstats=user1vendorstats,
                           user2getlevel=user2getlevel,
                           user2pictureid=user2pictureid,
                           user2stats=user2stats,
                           user2wallet=user2wallet,
                           user2level=user2level,
                           user2width=user2width,
                           user2ach=user2ach,
                           user2vendorstats=user2vendorstats,
                           user2=user2,
                           )
