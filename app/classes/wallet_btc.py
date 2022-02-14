from app import db
from datetime import datetime


class Btc_Prices(db.Model):
    __tablename__ = 'prices_btc'
    __bind_key__ = 'avengers'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.DECIMAL(50, 2))


class Btc_Wallet(db.Model):
    __tablename__ = 'btc_wallet'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    currentbalance = db.Column(db.DECIMAL(20, 8))
    address1 = db.Column(db.TEXT)
    address1status = db.Column(db.INTEGER)
    address2 = db.Column(db.TEXT)
    address2status = db.Column(db.INTEGER)
    address3 = db.Column(db.TEXT)
    address3status = db.Column(db.INTEGER)
    locked = db.Column(db.INTEGER)
    transactioncount = db.Column(db.INTEGER)
    unconfirmed = db.Column(db.DECIMAL(20, 8))


class Btc_Unconfirmed(db.Model):
    __tablename__ = 'btc_unconfirmed'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)

    unconfirmed1 = db.Column(db.DECIMAL(20, 8))
    unconfirmed2 = db.Column(db.DECIMAL(20, 8))
    unconfirmed3 = db.Column(db.DECIMAL(20, 8))
    unconfirmed4 = db.Column(db.DECIMAL(20, 8))
    unconfirmed5 = db.Column(db.DECIMAL(20, 8))

    txid1 = db.Column(db.TEXT)
    txid2 = db.Column(db.TEXT)
    txid3 = db.Column(db.TEXT)
    txid4 = db.Column(db.TEXT)
    txid5 = db.Column(db.TEXT)


class Btc_WalletWork(db.Model):
    __tablename__ = 'btc_walletwork'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    amount = db.Column(db.DECIMAL(20, 8))
    sendto = db.Column(db.TEXT)
    comment = db.Column(db.TEXT)
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    txtcomment = db.Column(db.TEXT)


class Btc_WalletAddresses(db.Model):
    __tablename__ = 'btc_walletaddresses'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btcaddress = db.Column(db.TEXT)
    status = db.Column(db.INTEGER)


class Btc_TransactionsBtc(db.Model):
    __tablename__ = 'btc_transactions'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    category = db.Column(db.INTEGER)
    senderid = db.Column(db.INTEGER)
    confirmations = db.Column(db.INTEGER)
    txid = db.Column(db.TEXT)
    amount = db.Column(db.DECIMAL(20, 8))
    blockhash = db.Column(db.TEXT)
    timeoft = db.Column(db.INTEGER)
    timerecieved = db.Column(db.INTEGER)
    commentbtc = db.Column(db.TEXT)
    otheraccount = db.Column(db.INTEGER)
    address = db.Column(db.TEXT)
    fee = db.Column(db.DECIMAL(20, 8))
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    balance = db.Column(db.DECIMAL(20, 8))
    orderid = db.Column(db.INTEGER)
    confirmed = db.Column(db.INTEGER)
    confirmed_fee = db.Column(db.DECIMAL(20, 8))
    digital_currency = db.Column(db.INTEGER)


class Btc_WalletFee(db.Model):
    __tablename__ = 'btc_walletfee'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btc = db.Column(db.DECIMAL(20, 8))


class Btc_TransOrphan(db.Model):
    __tablename__ = 'btc_transorphan'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btc = db.Column(db.DECIMAL(20, 8))
    btcaddress = db.Column(db.TEXT)
    txid = db.Column(db.TEXT)
