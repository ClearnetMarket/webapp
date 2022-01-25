# coding=utf-8
from app import db


class Orders(db.Model):
    __tablename__ = 'orders'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", "extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    type = db.Column(db.INTEGER)
    vendor = db.Column(db.TEXT)
    vendor_id = db.Column(db.INTEGER)
    customer = db.Column(db.TEXT)
    customer_id = db.Column(db.INTEGER)
    currency = db.Column(db.INTEGER)
    incart = db.Column(db.INTEGER)
    new_order = db.Column(db.INTEGER)
    accepted_order = db.Column(db.INTEGER)
    waiting_order = db.Column(db.INTEGER)
    disputed_order = db.Column(db.INTEGER)
    disputedtimer = db.Column(db.TIMESTAMP())
    modid = db.Column(db.INTEGER)
    delivered_order = db.Column(db.INTEGER)
    title = db.Column(db.TEXT)

    age = db.Column(db.TIMESTAMP())
    returncancelage = db.Column(db.TIMESTAMP())
    return_by = db.Column(db.TIMESTAMP())
    private_note = db.Column(db.TEXT)
    escrow = db.Column(db.TEXT)
    item_id = db.Column(db.INTEGER)
    stringauctionid = db.Column(db.TEXT)
    stringnodeid = db.Column(db.TEXT)
    imageone = db.Column(db.TEXT)
    quantity = db.Column(db.INTEGER)
    request_cancel = db.Column(db.INTEGER)
    reason_cancel = db.Column(db.INTEGER)
    cancelled = db.Column(db.INTEGER)
    request_return = db.Column(db.INTEGER)
    shipping_price = db.Column(db.DECIMAL(20, 8))
    shipdescription = db.Column(db.TEXT)
    overallreason = db.Column(db.TEXT)
    return_id = db.Column(db.INTEGER)
    return_quantity = db.Column(db.INTEGER)
    return_amount = db.Column(db.DECIMAL(20, 8))
    feedback = db.Column(db.INTEGER)
    userfeedback = db.Column(db.INTEGER)
    completed = db.Column(db.INTEGER)
    perbtc = db.Column(db.DECIMAL(20, 2))

    completed_time = db.Column(db.TIMESTAMP())
    return_allowed = db.Column(db.INTEGER)
    buyorsell = db.Column(db.INTEGER)
    released = db.Column(db.INTEGER)

    digital_currency = db.Column(db.INTEGER)
    fee = db.Column(db.DECIMAL(20, 8))
    price = db.Column(db.DECIMAL(20, 8))
    price_peritem = db.Column(db.DECIMAL(20, 8))
    price_beforediscount = db.Column(db.DECIMAL(20, 8))
    # affiliate stuff

    affiliate_discount_percent = db.Column(db.DECIMAL(4, 2))
    affiliate_code = db.Column(db.TEXT)
    affiliate_profit = db.Column(db.DECIMAL(20, 8))
    affiliate_discount_btc = db.Column(db.DECIMAL(20, 8))
    affiliate_discount_btc_cash = db.Column(db.DECIMAL(20, 8))


class AffiliateOverview(db.Model):
    __tablename__ = 'affiliate_overview'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, unique=True)
    userid = db.Column(db.INTEGER)

    # the discount the buyer gets
    buyerdiscount = db.Column(db.DECIMAL(6, 2))
    buyerdiscount_time = db.Column(db.TIMESTAMP())

    # fee to pay the affiliate
    aff_fee = db.Column(db.DECIMAL(6, 2))
    aff_fee_time = db.Column(db.TIMESTAMP())

    # links to twitch or there website
    aff_link_1 = db.Column(db.TEXT)
    aff_link_2 = db.Column(db.TEXT)
    promocode = db.Column(db.TEXT)


class AffiliateStats(db.Model):
    __tablename__ = 'affiliate_stats'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, unique=True)
    userid = db.Column(db.INTEGER)
    # how many items ordered
    totalitemsordered = db.Column(db.INTEGER)

    # how many times entered the promo code
    promoenteredcount = db.Column(db.INTEGER)

    # BTC Earned
    btc_earned = db.Column(db.DECIMAL(20, 8))

    # BTC CASH Earned
    btc_cash_earned = db.Column(db.DECIMAL(20, 8))
    # promocode
    promocode = db.Column(db.TEXT)


class AffiliateId(db.Model):
    __tablename__ = 'affiliate_ids'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, unique=True)
    userid = db.Column(db.INTEGER)
    promocode = db.Column(db.TEXT)


db.configure_mappers()
db.create_all()
db.session.commit()
