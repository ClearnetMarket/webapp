from flask import render_template,redirect, url_for, flash, request
from flask_login import current_user

from app.wallet_xmr import wallet_xmr
from app import db, app

from decimal import Decimal
from app.common.functions import floating_decimals
from app.common.decorators import login_required

from app.wallet_xmr.monero_wallet_work import\
    xmr_create_wallet,\
    xmr_send_coin
from app.wallet_xmr.forms import WalletSendCoin
# Models
from app.classes.wallet_xmr import \
    Xmr_Wallet, \
    Xmr_WalletFee, \
    Xmr_Transactions,\
    Xmr_WalletWork
from app.classes.auth import Auth_User
from app.classes.message import Message_Notifications


@wallet_xmr.route('', methods=['GET'])
@login_required
def home():
    # forms
    form = WalletSendCoin()

    # Get wallet
    wallet = db.session.query(Xmr_Wallet).filter_by(user_id=current_user.id).first()
    if wallet is None:
        xmr_create_wallet(user_id=current_user.id)
    if wallet.address1status == 0:
        xmr_create_wallet(user_id=current_user.id)

    # get unread messages
    if current_user.is_authenticated:
        thenotes = db.session\
            .query(Message_Notifications)\
            .filter(Message_Notifications.user_id == current_user.id)\
            .order_by(Message_Notifications.timestamp.desc())
        thenotescount = thenotes.filter(Message_Notifications.read == 0)
        thenotescount = thenotescount.count()
        thenotes = thenotes.limit(25)
    else:
        thenotes = 0
        thenotescount = 0

    walletwork = db.session\
        .query(Xmr_WalletWork)\
        .filter_by(user_id=current_user.id)\
        .first()
    # walletfee
    walletthefee = db.session.query(Xmr_WalletFee).get(1)
    wfee = Decimal(walletthefee.amount)

    # Get Transaction history
    page = request.args.get('page', 1, type=int)
    transactfull = db.session\
        .query(Xmr_Transactions)\
        .filter(Xmr_Transactions.user_id == current_user.id)\
        .filter(Xmr_Transactions.digital_currency == 4)\
        .order_by(Xmr_Transactions.id.desc())
    transactcount = transactfull.count()
    transactfull = transactfull.paginate(page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('wallet_xmr.home', page=transactfull.next_num) \
        if transactfull.has_next else None
    prev_url = url_for('wallet_xmr.home', page=transactfull.prev_num) \
        if transactfull.has_prev else None

    return render_template('wallet_xmr/home.html',
                           # forms
                           form=form,
                           # wallet
                           wallet=wallet,
                           walletwork=walletwork,
                           thenotes=thenotes,
                           thenotescount=thenotescount,
                           wfee=wfee,
                           # transactions
                           transactcount=transactcount,
                           transact=transactfull.items,
                           next_url=next_url,
                           prev_url=prev_url,

                           )


@wallet_xmr.route('/sendxmr', methods=['POST'])
@login_required
def sendcoin():
    # forms
    form = WalletSendCoin()
    # Get wallet
    wallet = db.session\
        .query(Xmr_WalletFee)\
        .filter_by(user_id=current_user.id)\
        .first()
    # walletfee
    walletthefee = db.session\
        .query(Xmr_WalletFee)\
        .get(1)
    wfee = Decimal(walletthefee.amount)

    if request.method == "POST":
        if form.validate_on_submit():

            if Auth_User.decryptpassword(pwdhash=current_user.wallet_pin,
                                         password=form.pin.data):
                sendto = form.sendto.data
                amount = form.amount.data

                # test wallet_btc stuff for security
                walbal = Decimal(wallet.currentbalance)
                amount2withfee = Decimal(amount) + Decimal(wfee)
                # greater than amount with fee
                if floating_decimals(walbal, 8) >= floating_decimals(amount2withfee, 8):
                    # greater than fee
                    if Decimal(amount) > Decimal(wfee):
                        # add to wallet_btc work
                        xmr_send_coin(
                            user_id=current_user.id,
                            sendto=sendto,
                            amount=amount,
                        )
                        flash(f"XMR Sent:  {str(sendto)}", category="success")
                        flash("Please allow a few minutes for the transaction"
                              " to appear and process to begin.",
                              category="success")
                        return redirect(url_for('wallet_xmr.home', user_name=current_user.user_name))
                    else:
                        flash(f"Cannot withdraw amount less than wallet_btc fee: {str(wfee)}", category="danger")
                        return redirect(url_for('wallet_xmr.home', user_name=current_user.user_name))
                else:
                    flash(f"Cannot withdraw amount less than wallet_btc fee: {str(wfee)}", category="danger")
                    return redirect(url_for('wallet_xmr.home', user_name=current_user.user_name))
            else:
                flash("Invalid Pin.", category="danger")
                return redirect(url_for('wallet_xmr.home', user_name=current_user.user_name))
        else:
            flash("Bad Form.  Did you enter the information correctly?", category="danger")
            return redirect(url_for('wallet_xmr.home', user_name=current_user.user_name))
