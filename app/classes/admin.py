from app import db


class clearnetFee(db.Model):
    __tablename__ = 'fees'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    itempurchase = db.Column(db.DECIMAL(20, 2))


class clearnetprofit_btc(db.Model):
    __tablename__ = 'account_profit_btc'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    order = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 8))


class clearnetprofit_btccash(db.Model):
    __tablename__ = 'account_profit_btccash'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    order = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 8))


class clearnetfeeholdings(db.Model):
    __tablename__ = 'account_fee_holdings_btc'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 8))


class clearnetfeeholdings_btccash(db.Model):
    __tablename__ = 'account_fee_holdings_btc_cash'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.TIMESTAMP(), index=True)
    total = db.Column(db.DECIMAL(20, 8))


class clearnetholdings(db.Model):
    __tablename__ = 'account_clearnetholdings_btc'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER)
    total = db.Column(db.DECIMAL(20, 8))


class clearnetholdings_btccash(db.Model):
    __tablename__ = 'account_clearnetholdings_btc_cash'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    amount = db.Column(db.DECIMAL(20, 8))
    timestamp = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER)
    total = db.Column(db.DECIMAL(20, 8))


class Recaptcha(db.Model):
    __tablename__ = 'recaptcha'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    image = db.Column(db.INTEGER)
    answer = db.Column(db.TEXT)


class websiteOffline(db.Model):
    __tablename__ = 'websiteoffline'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    webstatus = db.Column(db.INTEGER)


class flagged(db.Model):
    __tablename__ = 'flagged'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    user_id = db.Column(db.INTEGER)
    vendorname = db.Column(db.TEXT)
    howmany = db.Column(db.INTEGER)
    typeitem = db.Column(db.INTEGER)
    listingid = db.Column(db.INTEGER)
    listingtitle = db.Column(db.INTEGER)
    flaggeduser_id1 = db.Column(db.INTEGER)
    flaggeduser_id2 = db.Column(db.INTEGER)
    flaggeduser_id3 = db.Column(db.INTEGER)
    flaggeduser_id4 = db.Column(db.INTEGER)
    flaggeduser_id5 = db.Column(db.INTEGER)


db.configure_mappers()
db.create_all()
db.session.commit()
