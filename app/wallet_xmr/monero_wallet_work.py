from datetime import datetime
from decimal import Decimal
from app import db
from app.common.functions import floating_decimals
from app.notification import notification

from app.wallet_xmr.security import xmr_check_balance
from app.classes.wallet_xmr import \
    Xmr_Wallet, \
    Xmr_WalletWork, \
    Xmr_WalletFee, \
    Xmr_Unconfirmed

def xmr_create_wallet(user_id):
    """
    This creates the wallet and gives it a random payment id for
    deposites
    :param user_id:
    :return:
    """
    timestamp = datetime.utcnow()

    monero_newunconfirmed = Xmr_Unconfirmed(
        user_id=user_id,
        unconfirmed1=0,
        unconfirmed2=0,
        unconfirmed3=0,
        unconfirmed4=0,
        unconfirmed5=0,
        txid1='',
        txid2='',
        txid3='',
        txid4='',
        txid5='',
    )

    # creates wallet_btc in db
    monero_walletcreate = Xmr_Wallet(user_id=user_id,
                                       currentbalance=0,
                                       unconfirmed=0,
                                       address1='',
                                       address1status=1,
                                       locked=0,
                                       transactioncount=0,
                                       )
    wallet = Xmr_WalletWork(
        user_id=user_id,
        type=2,
        amount=0,
        sendto='',
        txnumber=0,
        created=timestamp,

    )
    db.session.add(wallet)
    db.session.add(monero_newunconfirmed)
    db.session.add(monero_walletcreate)




def xmr_wallet_status(user_id):
    """
    This will check if the wallet is normal,
    if not it creates a new wallet
    :param user_id:
    :return:
    """
    userwallet = db.session.query(Xmr_Wallet).filter_by(user_id=user_id).first()

    if userwallet:
        pass
    else:
        xmr_create_wallet(user_id=user_id)


def xmr_send_coin(user_id, sendto, amount):
    """
    # OFF SITE
    # withdrawl
    :param user_id:
    :param sendto:
    :param amount:
    :return:
    """
    getwallet = Xmr_WalletFee.query.get(1)
    walletfee = getwallet.amount
    a = xmr_check_balance(user_id=user_id, amount=amount)
    if a == 1:

        timestamp = datetime.utcnow()
        userswallet = db.session.query(Xmr_Wallet).filter_by(user_id=user_id).first()
        # turn sting to a decimal
        amountdecimal = Decimal(amount)
        # make decimal 8th power
        amounttomod = floating_decimals(amountdecimal, 8)
        # gets current balance
        curbalance = floating_decimals(userswallet.currentbalance, 8)
        # gets amount and fee
        amountandfee = floating_decimals(amounttomod + walletfee, 8)
        # subtracts amount and fee from current balance
        y = floating_decimals(curbalance - amountandfee, 8)
        # set balance as new amount
        userswallet.currentbalance = floating_decimals(y, 8)
        wallet = Xmr_WalletWork(
            user_id=user_id,
            type=1,
            amount=amount,
            sendto=sendto,
            created=timestamp,
        )
        db.session.add(wallet)
        db.session.add(userswallet)
    else:
        notification(user_id=user_id,
                             subid=0,
                             subname='',
                             postid=0,
                             commentid=0,
                             msg=34)
