from app import db
from datetime import datetime


class Bch_Wallet(db.Model):
    __tablename__ = 'bch_wallet'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
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
    shard = db.Column(db.INTEGER)


class Bch_Prices(db.Model):
    __tablename__ = 'bch_price'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.DECIMAL(50, 2))
    currency_id = db.Column(db.INTEGER)
    percent_change_twentyfour = db.Column(db.DECIMAL(50, 2))


class Bch_WalletTransferOrphan(db.Model):
    __tablename__ = 'bch_transaction_orphan'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bch = db.Column(db.DECIMAL(20, 8))
    bchaddress = db.Column(db.VARCHAR(500))
    txid = db.Column(db.VARCHAR(500))


class Bch_WalletUnconfirmed(db.Model):
    __tablename__ = 'bch_wallet_unconfirmed_transaction'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
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


class Bch_WalletWork(db.Model):
    __tablename__ = 'bch_wallet_work'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    amount = db.Column(db.DECIMAL(20, 8))
    sendto = db.Column(db.VARCHAR(500))
    comment = db.Column(db.VARCHAR(500))
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    txtcomment = db.Column(db.VARCHAR(500))


class Bch_WalletAddresses(db.Model):
    __tablename__ = 'bch_wallet_addresses'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bchaddress = db.Column(db.VARCHAR(500))
    status = db.Column(db.INTEGER)
    shard = db.Column(db.INTEGER)


class Bch_WalletFee(db.Model):
    __tablename__ = 'bch_wallet_fee'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bch = db.Column(db.DECIMAL(20, 8))


class Bch_WalletTransactions(db.Model):
    __tablename__ = 'bch_transactions'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER)
    senderid = db.Column(db.INTEGER)
    confirmations = db.Column(db.INTEGER)
    txid = db.Column(db.VARCHAR(500))
    amount = db.Column(db.DECIMAL(20, 8))
    blockhash = db.Column(db.VARCHAR(500))
    timeoft = db.Column(db.INTEGER)
    timerecieved = db.Column(db.INTEGER)
    commentbch = db.Column(db.VARCHAR(500))
    otheraccount = db.Column(db.INTEGER)
    address = db.Column(db.VARCHAR(500))
    fee = db.Column(db.DECIMAL(20, 8))
    created = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    balance = db.Column(db.DECIMAL(20, 8))
    orderid = db.Column(db.INTEGER)
    confirmed = db.Column(db.INTEGER)
    confirmed_fee = db.Column(db.DECIMAL(20, 8))
    digital_currency = db.Column(db.INTEGER)


db.configure_mappers()
db.create_all()
db.session.commit()
