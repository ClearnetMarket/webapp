from app import \
    db

from app.common.functions import \
    floating_decimals
from app.notification import \
    notification
from app.wallet_btccash.wallet_btccash_transaction import \
    btc_cash_addtransaction
from app.wallet_btccash.wallet_btccash_security import \
    checkbalance_btccash
from decimal import Decimal

# models
from app.classes.auth import \
    User

from app.classes.admin import \
    clearnetprofit_btccash, \
    clearnetholdings_btccash

from app.classes.wallet_bch import *
from app.classes.auth import UserFees
# end models


def btc_cash_walletstatus(userid):
    """
    This function checks status opf the wallet
    :param userid:
    :return:
    """
    userswallet = db.session\
        .query(BchWallet)\
        .filter_by(userid=userid)\
        .first()
    getuser = db.session\
        .query(User)\
        .filter(User.id == userid)\
        .first()
    if userswallet:
        try:
            if userswallet.address1status == 0 and userswallet.address2status == 0 and userswallet.address2status == 0:
                btc_cash_create_wallet(userid=userid)
                if getuser.shard is None:
                    getuser.shard = 1
                    db.session.add(getuser)

        except Exception as e:
            userswallet.address1 = ''
            userswallet.address1status = 0
            userswallet.address2 = ''
            userswallet.address2status = 0
            userswallet.address3 = ''
            userswallet.address3status = 0

            db.session.add(userswallet)
    else:
        # creates wallet_btc in db
        btc_cash_create_wallet(userid=getuser.id)


def btc_cash_create_wallet(userid):
    """
    This function creates the wallet_btccash and puts its first address there
    if wallet exists it adds an address to wallet
    :param userid:
    :return:
    """

    userswallet = db.session\
                    .query(BchWallet)\
                    .filter_by(userid=userid)\
                    .first()

    if userswallet:
        # find a new clean address
        getnewaddress = db.session\
                        .query(BchWalletAddresses) \
                        .filter(BchWalletAddresses.status == 0, BchWalletAddresses.shard == userswallet.shard) \
                        .first()

        # sets users wallet with this
        userswallet.address1 = getnewaddress.btcaddress
        userswallet.address1status = 1
        db.session.add(userswallet)

        # update address in listing as used
        getnewaddress.shard = 1
        getnewaddress.userid = userid
        getnewaddress.status = 1
        db.session.add(getnewaddress)

    else:
        # create a new wallet
        btc_cash_walletcreate = BchWallet(userid=userid,
                                          currentbalance=0,
                                          unconfirmed=0,
                                          address1='',
                                          address1status=0,
                                          address2='',
                                          address2status=0,
                                          address3='',
                                          address3status=0,
                                          locked=0,
                                          shard=1,
                                          transactioncount=0
                                          )
        db.session.add(btc_cash_walletcreate)

        btc_cash_newunconfirmed = BchUnconfirmed(
            userid=userid,
            unconfirmed1=0,
            unconfirmed2=0,
            unconfirmed3=0,
            unconfirmed4=0,
            unconfirmed5=0,
            unconfirmed6=0,
            unconfirmed7=0,
            unconfirmed8=0,
            unconfirmed9=0,
            unconfirmed10=0,
            txid1='',
            txid2='',
            txid3='',
            txid4='',
            txid5='',
            txid6='',
            txid7='',
            txid8='',
            txid9='',
            txid10='',
        )
        db.session.add(btc_cash_newunconfirmed)

        getnewaddress = db.session \
                .query(BchWalletAddresses) \
                .filter(BchWalletAddresses.status == 0,BchWalletAddresses.shard == userswallet.shard) \
                .first()

        userswallet.address1 = getnewaddress.btcaddress
        userswallet.address1status = 1
        db.session.add(userswallet)

        getnewaddress.shard = 1
        getnewaddress.userid = userid
        getnewaddress.status = 1
        db.session.add(getnewaddress)


def btc_cash_sendCoin(userid, sendto, amount, comment):
    """
    Add work order to send off site
    :param userid:
    :param sendto:
    :param amount:
    :param comment:
    :return:
    """
    timestamp = datetime.utcnow()
    getwallet = db.session\
        .query(BchWalletFee)\
        .filter_by(id=1)\
        .first()
    walletfee = getwallet.btc
    a = checkbalance_btccash(userid=userid, amount=amount)
    if a == 1:

        strcomment = str(comment)
        type_transaction = 2
        userswallet = db.session\
            .query(BchWallet)\
            .filter_by(userid=userid)\
            .first()

        wallet = BchWalletWork(
            userid=userid,
            type=type_transaction,
            amount=amount,
            sendto=sendto,
            comment=0,
            created=timestamp,
            txtcomment=strcomment,
            shard=userswallet.shard
        )

        db.session.add(wallet)

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

        db.session.add(userswallet)


    else:
        notification(
            type=34,
            username='',
            userid=userid,
            salenumber=0,
            bitcoin=amount
        )



def btc_cash_sendCointoEscrow(amount, comment, userid):
    """
    # TO clearnet_webapp Wallet
    # this function will move the coin to clearnets wallet_btc from a user
    :param amount:
    :param comment:
    :param userid:
    :return:
    """
    a = checkbalance_btccash(userid=userid, amount=amount)
    if a == 1:
        try:
            type_transaction = 4
            userswallet = db.session.query(BchWallet).filter_by(userid=userid).first()
            curbal = Decimal(userswallet.currentbalance)
            amounttomod = Decimal(amount)
            newbalance = Decimal(curbal) - Decimal(amounttomod)
            userswallet.currentbalance = newbalance
            db.session.add(userswallet)
            
            oid = int(comment)
            btc_cash_addtransaction(category=type_transaction,
                                    amount=amount,
                                    userid=userid,
                                    comment='Sent Coin To Escrow',
                                    shard=userswallet.shard,
                                    orderid=oid,
                                    balance=newbalance
                                    )

        except Exception as e:
            print(str(e))
            notification(
                type=34,
                username='',
                userid=userid,
                salenumber=comment,
                bitcoin=amount
            )

    else:
        print("a equals", a)
        notification(
            type=34,
            username='',
            userid=userid,
            salenumber=comment,
            bitcoin=amount
        )



def btc_cash_send_coin_to_user_as_admin(amount, comment, userid):
    """
    #to User
    # this function will move the coin from clearnets wallet_btc to a user as an admin
    :param amount:
    :param comment:
    :param userid:
    :return:
    """

    type_transaction = 9

    userswallet = db.session.query(BchWallet).filter_by(userid=userid).first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) + Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)
    db.session.flush()

    btc_cash_addtransaction(category=type_transaction,
                            amount=amount,
                            userid=userid,
                            comment=comment,
                            shard=userswallet.shard,
                            orderid=0,
                            balance=newbalance
                            )


def btc_cash_takeCointoUser_asAdmin(amount, comment, userid):
    """
    # TO User
    # this function will move the coin from clearnets wallet_btc to a user as an admin
    :param amount:
    :param comment:
    :param userid:
    :return:
    """

    type_transaction = 10
    a = Decimal(amount)
    userswallet = db.session.query(BchWallet).filter_by(userid=userid).first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) - Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)
    db.session.flush()

    btc_cash_addtransaction(category=type_transaction,
                            amount=amount,
                            userid=userid,
                            comment=comment,
                            shard=userswallet.shard,
                            orderid=0,
                            balance=newbalance
                            )

    getcurrentprofit = db.session\
        .query(clearnetprofit_btccash)\
        .order_by(clearnetprofit_btccash.id.desc())\
        .first()
    currentamount = floating_decimals(getcurrentprofit.total, 8)
    newamount = floating_decimals(currentamount, 8) + floating_decimals(a, 8)
    prof = clearnetprofit_btccash(
        amount=amount,
        timestamp=datetime.utcnow(),
        total=newamount
    )
    db.session.add(prof)


def sendcoinforad(amount, userid, comment):
    """
    # TO clearnet_webapp
    # this function will move the coin from vendor to clearnet holdings.  This is for vendor verification
    :param amount:
    :param userid:
    :param comment:
    :return:
    """
    a = checkbalance_btccash(userid=userid, amount=amount)
    if a == 1:
        type_transaction = 9
        now = datetime.utcnow()
        user = db.session\
            .query(User)\
            .filter(User.id == userid)\
            .first()
        userswallet = db.session\
            .query(BchWallet)\
            .filter_by(userid=userid)\
            .first()
        curbal = Decimal(userswallet.currentbalance)
        amounttomod = floating_decimals(amount, 8)
        newbalance = floating_decimals(curbal, 8) - floating_decimals(amounttomod, 8)
        userswallet.currentbalance = newbalance
        db.session.add(userswallet)
        db.session.flush()

        c = str(comment)
        a = Decimal(amount)
        commentstring = "Sent money for ad " + c
        btc_cash_addtransaction(category=type_transaction,
                                amount=amount,
                                userid=user.id,
                                comment=commentstring,
                                shard=user.shard_btccash,
                                orderid=0,
                                balance=newbalance
                                )

        getcurrentholdings = db.session\
            .query(clearnetholdings_btccash)\
            .order_by(clearnetholdings_btccash.id.desc())\
            .first()
        currentamount = floating_decimals(getcurrentholdings.total, 8)
        newamount = floating_decimals(
            currentamount, 8) + floating_decimals(a, 8)

        holdingsaccount = clearnetholdings_btccash(
            amount=a,
            timestamp=now,
            userid=userid,
            total=newamount
        )

        db.session.add(holdingsaccount)


def btc_cash_sendCointoHoldings(amount, userid, comment):
    """
    # TO clearnet_webapp
    # this function will move the coin from vendor to clearnet holdings.  This is for vendor verification
    :param amount:
    :param userid:
    :param comment:
    :return:
    """
    a = checkbalance_btccash(userid=userid, amount=amount)
    if a == 1:
        type_transaction = 7
        now = datetime.utcnow()
        user = db.session\
            .query(User)\
            .filter(User.id == userid)\
            .first()
        userswallet = db.session\
            .query(BchWallet)\
            .filter_by(userid=userid)\
            .first()
        curbal = Decimal(userswallet.currentbalance)
        amounttomod = floating_decimals(amount, 8)
        newbalance = floating_decimals(curbal, 8) - floating_decimals(amounttomod, 8)
        userswallet.currentbalance = newbalance
        db.session.add(userswallet)
        db.session.flush()

        c = str(comment)
        a = Decimal(amount)
        commentstring = "Vendor Verification: Level " + c
        btc_cash_addtransaction(category=type_transaction,
                                amount=amount,
                                userid=user.id,
                                comment=commentstring,
                                shard=user.shard_btccash,
                                orderid=0,
                                balance=newbalance
                                )

        getcurrentholdings = db.session\
            .query(clearnetholdings_btccash)\
            .order_by(clearnetholdings_btccash.id.desc())\
            .first()
        currentamount = floating_decimals(getcurrentholdings.total, 8)
        newamount = floating_decimals(currentamount, 8) + floating_decimals(a, 8)

        holdingsaccount = clearnetholdings_btccash(
            amount=a,
            timestamp=now,
            userid=userid,
            total=newamount
        )

        db.session.add(holdingsaccount)



def btc_cash_sendCoinfromHoldings(amount, userid, comment):
    """
    # TO clearnet_webapp
    # this function will move the coin from holdings back to vendor.  This is for vendor verification
    :param amount:
    :param userid:
    :param comment:
    :return:
    """

    type_transaction = 8
    now = datetime.utcnow()
    user = db.session\
        .query(User)\
        .filter(User.id == userid)\
        .first()
    userswallet = db.session\
        .query(BchWallet)\
        .filter_by(userid=userid)\
        .first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) + Decimal(amounttomod)
    userswallet.currentbalance = newbalance

    db.session.add(userswallet)
    db.session.flush()

    c = str(comment)
    a = Decimal(amount)
    commentstring = "Vendor Verification Refund: Level " + c

    btc_cash_addtransaction(category=type_transaction,
                            amount=amount,
                            userid=user.id,
                            comment=commentstring,
                            shard=user.shard_btccash,
                            orderid=0,
                            balance=newbalance
                            )

    getcurrentholdings = db.session.query(clearnetholdings_btccash).order_by(
        clearnetholdings_btccash.id.desc()).first()
    currentamount = floating_decimals(getcurrentholdings.total, 8)
    newamount = floating_decimals(currentamount, 8) - floating_decimals(a, 8)

    holdingsaccount = clearnetholdings_btccash(
        amount=a,
        timestamp=now,
        userid=userid,
        total=newamount
    )
    db.session.add(holdingsaccount)



def btc_cash_sendCointoclearnet(amount, comment, shard):
    """
    # TO clearnet_webapp
    # this function will move the coin from clearnets escrow to profit account
    # no balance necessary
    :param amount:
    :param comment:
    :param shard:
    :return:
    """

    type_transaction = 6
    now = datetime.utcnow()
    oid = int(comment)
    a = Decimal(amount)
    btc_cash_addtransaction(
        category=type_transaction,
        amount=amount,
        userid=1,
        comment='Sent Coin to clearnet_webapp profit',
        shard=shard,
        orderid=oid,
        balance=0
    )

    getcurrentprofit = db.session\
        .query(clearnetprofit_btccash)\
        .order_by(clearnetprofit_btccash.id.desc())\
        .first()
    currentamount = floating_decimals(getcurrentprofit.total, 8)
    newamount = floating_decimals(currentamount, 8) + floating_decimals(a, 8)
    prof = clearnetprofit_btccash(
        amount=amount,
        order=oid,
        timestamp=now,
        total=newamount
    )
    db.session.add(prof)



def btc_cash_sendCointoUser(amount, comment, userid):
    """
    #TO User
    ##this function will move the coin from clearnets wallet_btc to a user
    :param amount:
    :param comment:
    :param userid:
    :return:
    """

    type_transaction = 5
    oid = int(comment)

    userswallet = db.session.query(BchWallet).filter_by(userid=userid).first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) + Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)
    db.session.flush()

    btc_cash_addtransaction(category=type_transaction,
                            amount=amount,
                            userid=userid,
                            comment='Transaction',
                            shard=userswallet.shard,
                            orderid=oid,
                            balance=newbalance
                            )


def btc_cash_sendcointoaffiliate(amount, comment, userid):
    """
    # TO clearnet_webapp
    # this function will move the coin from clearnets escrow to profit account
    # no balance necessary
    :param amount:
    :param comment:
    :param shard:
    :return:
    """

    type_transaction = 11

    oid = int(comment)

    userswallet = db.session.query(BchWallet).filter_by(userid=userid).first()
    curbal = Decimal(userswallet.currentbalance)
    amounttomod = Decimal(amount)
    newbalance = Decimal(curbal) + Decimal(amounttomod)
    userswallet.currentbalance = newbalance
    db.session.add(userswallet)


    btc_cash_addtransaction(category=type_transaction,
                            amount=amount,
                            userid=userid,
                            comment='Transaction',
                            shard=userswallet.shard,
                            orderid=oid,
                            balance=newbalance
                            )


