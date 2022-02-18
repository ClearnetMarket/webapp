from app import db
from datetime import datetime


class Btc_Prices(db.Model):
    __tablename__ = 'btc_prices'
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
    address1 = db.Column(db.VARCHAR(500))
    address1status = db.Column(db.INTEGER)
    address2 = db.Column(db.VARCHAR(500))
    address2status = db.Column(db.INTEGER)
    address3 = db.Column(db.VARCHAR(500))
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

    txid1 = db.Column(db.VARCHAR(500))
    txid2 = db.Column(db.VARCHAR(500))
    txid3 = db.Column(db.VARCHAR(500))
    txid4 = db.Column(db.VARCHAR(500))
    txid5 = db.Column(db.VARCHAR(500))


class Btc_WalletWork(db.Model):
    __tablename__ = 'btc_wallet_work'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    amount = db.Column(db.DECIMAL(20, 8))
    sendto = db.Column(db.VARCHAR(500))
    comment = db.Column(db.VARCHAR(500))
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    txtcomment = db.Column(db.VARCHAR(500))


class Btc_WalletAddresses(db.Model):
    __tablename__ = 'btc_wallet_addresses'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btcaddress = db.Column(db.VARCHAR(500))
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
    txid = db.Column(db.VARCHAR(500))
    amount = db.Column(db.DECIMAL(20, 8))
    blockhash = db.Column(db.VARCHAR(500))
    timeoft = db.Column(db.INTEGER)
    timerecieved = db.Column(db.INTEGER)
    commentbtc = db.Column(db.VARCHAR(500))
    otheraccount = db.Column(db.INTEGER)
    address = db.Column(db.VARCHAR(500))
    fee = db.Column(db.DECIMAL(20, 8))
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    balance = db.Column(db.DECIMAL(20, 8))
    orderid = db.Column(db.INTEGER)
    confirmed = db.Column(db.INTEGER)
    confirmed_fee = db.Column(db.DECIMAL(20, 8))
    digital_currency = db.Column(db.INTEGER)


class Btc_WalletFee(db.Model):
    __tablename__ = 'btc_wallet_fee'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btc = db.Column(db.DECIMAL(20, 8))


class Btc_TransOrphan(db.Model):
    __tablename__ = 'btc_transaction_orphan'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btc = db.Column(db.DECIMAL(20, 8))
    btcaddress = db.Column(db.VARCHAR(500))
    txid = db.Column(db.VARCHAR(500))
