from app import db


class Categories(db.Model):
    __tablename__ = 'category'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    name = db.Column(db.TEXT)


class ItemtoDelete(db.Model):
    __tablename__ = 'itemtodelete'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True, nullable=False)
    itemid = db.Column(db.Integer)


class ShoppingCart(db.Model):
    __tablename__ = 'shoppingcart'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    customer = db.Column(db.TEXT)
    customer_id = db.Column(db.INTEGER)
    vendor = db.Column(db.TEXT)
    vendor_id = db.Column(db.INTEGER)
    currency = db.Column(db.INTEGER)
    title_of_item = db.Column(db.TEXT)
    price_of_item = db.Column(db.DECIMAL(20, 2))
    stringauctionid = db.Column(db.TEXT)
    stringnodeid = db.Column(db.TEXT)
    image_of_item = db.Column(db.TEXT)
    quantity_of_item = db.Column(db.INTEGER)
    return_policy = db.Column(db.TEXT)
    savedforlater = db.Column(db.INTEGER)
    item_id = db.Column(db.INTEGER)
    vendorsupply = db.Column(db.INTEGER)
    shippinginfo0 = db.Column(db.TEXT)
    shippingdayleast0 = db.Column(db.INTEGER)
    shippingdaymost0 = db.Column(db.INTEGER)
    shippinginfo2 = db.Column(db.TEXT)
    shippingprice2 = db.Column(db.DECIMAL(20, 2))
    shippingdayleast2 = db.Column(db.INTEGER)
    shippingdaymost2 = db.Column(db.INTEGER)
    shippinginfo3 = db.Column(db.TEXT)
    shippingprice3 = db.Column(db.DECIMAL(20, 2))
    shippingdayleast3 = db.Column(db.INTEGER)
    shippingdaymost3 = db.Column(db.INTEGER)
    shippingfree = db.Column(db.INTEGER)
    shippingtwo = db.Column(db.INTEGER)
    shippingthree = db.Column(db.INTEGER)
    return_allowed = db.Column(db.INTEGER)
    digital_currency1 = db.Column(db.INTEGER)
    digital_currency2 = db.Column(db.INTEGER)
    digital_currency3 = db.Column(db.INTEGER)
    selected_currency = db.Column(db.INTEGER)
    selected_shipping = db.Column(db.INTEGER)
    selected_shipping_description = db.Column(db.TEXT)
    final_shipping_price = db.Column(db.DECIMAL(20, 8))
    final_price = db.Column(db.DECIMAL(20, 8))


class ShoppingCartTotal(db.Model):
    __tablename__ = 'shoppingcarttotal'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    customer = db.Column(db.INTEGER)
    btc_sumofitem = db.Column(db.INTEGER)
    btcprice = db.Column(db.DECIMAL(20, 8))
    shippingbtcprice = db.Column(db.DECIMAL(20, 8))
    totalbtcprice = db.Column(db.DECIMAL(20, 8))
    btc_cash_sumofitem = db.Column(db.INTEGER)
    btc_cash_price = db.Column(db.DECIMAL(20, 8))
    shipping_btc_cashprice = db.Column(db.DECIMAL(20, 8))
    total_btc_cash_price = db.Column(db.DECIMAL(20, 8))
    # affiliate stuff
    percent_off_order = db.Column(db.DECIMAL(6, 2))
    btc_cash_off = db.Column(db.DECIMAL(20, 8))
    btc_off = db.Column(db.DECIMAL(20, 8))


class marketItem(db.Model):
    __tablename__ = 'marketitem'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True, nullable=False)

    online = db.Column(db.INTEGER)
    created = db.Column(db.TIMESTAMP())
    price = db.Column(db.DECIMAL(20, 2))
    vendor_name = db.Column(db.TEXT)
    vendor_id = db.Column(db.INTEGER)
    stringauctionid = db.Column(db.TEXT)
    stringnodeid = db.Column(db.TEXT)

    origincountry = db.Column(db.INTEGER)
    destinationcountry = db.Column(db.INTEGER)
    destinationcountrytwo = db.Column(db.INTEGER)
    destinationcountrythree = db.Column(db.INTEGER)
    destinationcountryfour = db.Column(db.INTEGER)
    destinationcountryfive = db.Column(db.INTEGER)

    itemtitlee = db.Column(db.TEXT)
    itemcount = db.Column(db.INTEGER)
    itemdescription = db.Column(db.TEXT)
    keywords = db.Column(db.TEXT)
    itemcondition = db.Column(db.INTEGER)

    itemrefundpolicy = db.Column(db.TEXT)
    return_allowed = db.Column(db.INTEGER)

    imageone = db.Column(db.TEXT)
    imagetwo = db.Column(db.TEXT)
    imagethree = db.Column(db.TEXT)
    imagefour = db.Column(db.TEXT)
    imagefive = db.Column(db.TEXT)

    details = db.Column(db.BOOLEAN)
    details1 = db.Column(db.TEXT)
    details1answer = db.Column(db.TEXT)
    details2 = db.Column(db.TEXT)
    details2answer = db.Column(db.TEXT)
    details3 = db.Column(db.TEXT)
    details3answer = db.Column(db.TEXT)
    details4 = db.Column(db.TEXT)
    details4answer = db.Column(db.TEXT)
    details5 = db.Column(db.TEXT)
    details5answer = db.Column(db.TEXT)

    viewcount = db.Column(db.INTEGER)
    itemrating = db.Column(db.DECIMAL(20, 2))
    reviewcount = db.Column(db.INTEGER)
    totalsold = db.Column(db.INTEGER)

    shippinginfo0 = db.Column(db.TEXT)
    shippingdayleast0 = db.Column(db.INTEGER)
    shippingdaymost0 = db.Column(db.INTEGER)
    shippinginfo2 = db.Column(db.TEXT)
    shippingprice2 = db.Column(db.DECIMAL(20, 2))
    shippingdayleast2 = db.Column(db.INTEGER)
    shippingdaymost2 = db.Column(db.INTEGER)
    shippinginfo3 = db.Column(db.TEXT)
    shippingprice3 = db.Column(db.DECIMAL(20, 2))
    shippingdayleast3 = db.Column(db.INTEGER)
    shippingdaymost3 = db.Column(db.INTEGER)

    notshipping1 = db.Column(db.INTEGER)
    notshipping2 = db.Column(db.INTEGER)
    notshipping3 = db.Column(db.INTEGER)
    notshipping4 = db.Column(db.INTEGER)
    notshipping5 = db.Column(db.INTEGER)
    notshipping6 = db.Column(db.INTEGER)
    shippingfree = db.Column(db.BOOLEAN)
    shippingtwo = db.Column(db.INTEGER)
    shippingthree = db.Column(db.INTEGER)

    currency = db.Column(db.INTEGER)
    digital_currency1 = db.Column(db.INTEGER)
    digital_currency2 = db.Column(db.INTEGER)
    digital_currency3 = db.Column(db.INTEGER)

    # Protos Item
    amazonid = db.Column(db.TEXT)
    amazon_last_checked = db.Column(db.TIMESTAMP())

    # categories
    categoryname0 = db.Column(db.TEXT)
    categoryid0 = db.Column(db.Integer)

    aditem = db.Column(db.INTEGER)
    aditem_level = db.Column(db.INTEGER)
    aditem_timer = db.Column(db.TIMESTAMP())

    def __str__(self):
        return 'marketItem %s' % self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Cats(db.Model):
    __tablename__ = 'cats'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", "extend_existing": True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True, nullable=False)
    catid0 = db.Column(db.Integer)
    catid0 = db.Column(db.Integer)
    catname0 = db.Column(db.TEXT)
    formname = db.Column(db.TEXT)


db.configure_mappers()
db.create_all()
db.session.commit()
