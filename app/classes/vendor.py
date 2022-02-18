from app import db
from uuid import uuid4


def get_uuid_item():
    return uuid4().hex



class Vendor_Orders(db.Model):
    __tablename__ = 'vendor_orders'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    uuid = db.Column(db.String(32), default=get_uuid_item)

    type = db.Column(db.INTEGER)
    vendor = db.Column(db.VARCHAR(40))
    vendor_id = db.Column(db.INTEGER)
    customer = db.Column(db.VARCHAR(40))
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
    title = db.Column(db.VARCHAR(500))
    age = db.Column(db.TIMESTAMP())
    returncancelage = db.Column(db.TIMESTAMP())
    return_by = db.Column(db.TIMESTAMP())
    private_note = db.Column(db.TEXT)
    escrow = db.Column(db.VARCHAR(500))
    item_id = db.Column(db.INTEGER)
    string_auction_id = db.Column(db.VARCHAR(50))
    string_node_id = db.Column(db.VARCHAR(50))
    image_one = db.Column(db.VARCHAR(100))
    quantity = db.Column(db.INTEGER)
    request_cancel = db.Column(db.INTEGER)
    reason_cancel = db.Column(db.INTEGER)
    cancelled = db.Column(db.INTEGER)
    request_return = db.Column(db.INTEGER)
    shipping_price = db.Column(db.DECIMAL(20, 8))
    shipdescription = db.Column(db.VARCHAR(500))
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
    price_peritem_btc = db.Column(db.DECIMAL(20, 8))
    price_beforediscount_btc = db.Column(db.DECIMAL(20, 8))
    price_peritem_bch = db.Column(db.DECIMAL(20, 8))
    price_beforediscount_bch = db.Column(db.DECIMAL(20, 8))
    price_peritem_xmr = db.Column(db.DECIMAL(20, 8))
    price_beforediscount_xmr = db.Column(db.DECIMAL(20, 8))
    # affiliate stuff
    affiliate_discount_percent = db.Column(db.DECIMAL(4, 2))
    affiliate_code = db.Column(db.VARCHAR(20))
    affiliate_profit = db.Column(db.DECIMAL(20, 8))
    affiliate_discount_btc = db.Column(db.DECIMAL(20, 8))
    affiliate_discount_btc_cash = db.Column(db.DECIMAL(20, 8))
    affiliate_discount_xmr = db.Column(db.DECIMAL(20, 12))


class Vendor_NotShipping(db.Model):
    __tablename__ = 'vendor_not_shipping_country'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    code = db.Column(db.INTEGER)
    name = db.Column(db.VARCHAR(40))


class Vendor_VendorVerification(db.Model):
    __tablename__ = 'vendor_verification_level'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_id = db.Column(db.INTEGER)
    vendor_level = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    amount = db.Column(db.DECIMAL(20, 8))


class Vendor_Duration(db.Model):
    __tablename__ = 'vendor_duration_timer'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    time = db.Column(db.VARCHAR(140))
    displaytime = db.Column(db.VARCHAR(140))


class Vendor_EbaySearchItem(db.Model):
    __tablename__ = 'vendor_ebay_item'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True, nullable=False)
    dateadded = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER)
    itemebayid = db.Column(db.BIGINT)
    itemtitle = db.Column(db.VARCHAR(500))
    itemprice = db.Column(db.DECIMAL(20, 4))
    itemquantity = db.Column(db.INTEGER)
    item_condition = db.Column(db.INTEGER)
    itemcategory = db.Column(db.VARCHAR(300))
    status = db.Column(db.INTEGER)
    errortext = db.Column(db.TEXT)


db.configure_mappers()
db.create_all()
db.session.commit()
