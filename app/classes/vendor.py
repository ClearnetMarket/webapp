from app import db


class Vendor_Orders(db.Model):
    __tablename__ = 'orders'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
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
    string_auction_id = db.Column(db.TEXT)
    string_node_id = db.Column(db.TEXT)
    image_one = db.Column(db.TEXT)
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


class Vendor_NotShipping(db.Model):
    __tablename__ = 'notshipping'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    code = db.Column(db.INTEGER)
    name = db.Column(db.TEXT)


class Vendor_VendorVerification(db.Model):
    __tablename__ = 'vendorverification'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_id = db.Column(db.INTEGER)
    vendor_level = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    amount = db.Column(db.DECIMAL(20, 8))


class Vendor_Duration(db.Model):
    __tablename__ = 'durations'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    time = db.Column(db.TEXT)
    displaytime = db.Column(db.TEXT)


class Vendor_EbaySearchItem(db.Model):
    __tablename__ = 'ebayitem'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True, nullable=False)
    dateadded = db.Column(db.TIMESTAMP())
    user_id = db.Column(db.INTEGER)
    itemebayid = db.Column(db.BIGINT)
    itemtitle = db.Column(db.TEXT)
    itemprice = db.Column(db.DECIMAL(20, 4))
    itemquantity = db.Column(db.INTEGER)
    item_condition = db.Column(db.INTEGER)
    itemcategory = db.Column(db.TEXT)
    status = db.Column(db.INTEGER)
    errortext = db.Column(db.TEXT)


db.configure_mappers()
db.create_all()
db.session.commit()
