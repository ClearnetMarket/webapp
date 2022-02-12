from app import db


class Item_ItemtoDelete(db.Model):
    __tablename__ = 'itemtodelete'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True, nullable=False)
    itemid = db.Column(db.Integer)


class Item_CheckoutShoppingCart(db.Model):
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
    string_auction_id = db.Column(db.TEXT)
    string_node_id = db.Column(db.TEXT)
    image_of_item = db.Column(db.TEXT)
    quantity_of_item = db.Column(db.INTEGER)
    return_policy = db.Column(db.TEXT)
    savedforlater = db.Column(db.INTEGER)
    item_id = db.Column(db.INTEGER)
    vendorsupply = db.Column(db.INTEGER)
    shipping_info_0 = db.Column(db.TEXT)
    shipping_day_least_0 = db.Column(db.INTEGER)
    shipping_day_most_0 = db.Column(db.INTEGER)
    shipping_info_2 = db.Column(db.TEXT)
    shipping_price_2 = db.Column(db.DECIMAL(20, 2))
    shipping_day_least_2 = db.Column(db.INTEGER)
    shipping_day_most_2 = db.Column(db.INTEGER)
    shipping_info_3 = db.Column(db.TEXT)
    shipping_price_3 = db.Column(db.DECIMAL(20, 2))
    shipping_day_least_3 = db.Column(db.INTEGER)
    shipping_day_most_3 = db.Column(db.INTEGER)
    shipping_free = db.Column(db.INTEGER)
    shipping_two = db.Column(db.INTEGER)
    shipping_three = db.Column(db.INTEGER)
    return_allowed = db.Column(db.INTEGER)
    digital_currency_1 = db.Column(db.INTEGER)
    digital_currency_2 = db.Column(db.INTEGER)
    digital_currency_3 = db.Column(db.INTEGER)
    selected_currency = db.Column(db.INTEGER)
    selected_shipping = db.Column(db.INTEGER)
    selected_shipping_description = db.Column(db.TEXT)
    final_shipping_price = db.Column(db.DECIMAL(20, 8))
    final_price = db.Column(db.DECIMAL(20, 8))


class Item_ShoppingCartTotal(db.Model):
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


class Item_MarketItem(db.Model):
    __tablename__ = 'marketitem'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True,
                   nullable=False)

    online = db.Column(db.INTEGER)
    created = db.Column(db.TIMESTAMP())
    price = db.Column(db.DECIMAL(20, 2))
    vendor_name = db.Column(db.String(140))
    vendor_id = db.Column(db.INTEGER)
    string_auction_id = db.Column(db.String(40))
    string_node_id = db.Column(db.String(40))

    origin_country = db.Column(db.INTEGER)
    destination_country_one = db.Column(db.INTEGER)
    destination_country_two = db.Column(db.INTEGER)
    destination_country_three = db.Column(db.INTEGER)
    destination_country_four = db.Column(db.INTEGER)
    destination_country_five = db.Column(db.INTEGER)

    item_title = db.Column(db.TEXT)
    item_count = db.Column(db.INTEGER)
    item_description = db.Column(db.TEXT)
    keywords = db.Column(db.TEXT)
    item_condition = db.Column(db.INTEGER)

    item_refund_policy = db.Column(db.TEXT)
    return_allowed = db.Column(db.INTEGER)

    image_one = db.Column(db.String(240))
    image_two = db.Column(db.String(240))
    image_three = db.Column(db.String(240))
    image_four = db.Column(db.String(240))
    image_five = db.Column(db.String(240))

    details = db.Column(db.BOOLEAN)
    details_1 = db.Column(db.TEXT)
    details_1_answer = db.Column(db.TEXT)
    details_2 = db.Column(db.TEXT)
    details_2_answer = db.Column(db.TEXT)
    details_3 = db.Column(db.TEXT)
    details_3_answer = db.Column(db.TEXT)
    details_4 = db.Column(db.TEXT)
    details_4_answer = db.Column(db.TEXT)
    details_5 = db.Column(db.TEXT)
    details_5_answer = db.Column(db.TEXT)

    view_count = db.Column(db.INTEGER)
    item_rating = db.Column(db.DECIMAL(20, 2))
    review_count = db.Column(db.INTEGER)
    total_sold = db.Column(db.INTEGER)

    shipping_free = db.Column(db.BOOLEAN)
    shipping_two = db.Column(db.BOOLEAN)
    shipping_three = db.Column(db.BOOLEAN)

    shipping_info_0 = db.Column(db.TEXT)
    shipping_day_least_0 = db.Column(db.INTEGER)
    shipping_day_most_0 = db.Column(db.INTEGER)
    shipping_info_2 = db.Column(db.TEXT)
    shipping_price_2 = db.Column(db.DECIMAL(20, 2))
    shipping_day_least_2 = db.Column(db.INTEGER)
    shipping_day_most_2 = db.Column(db.INTEGER)
    shipping_info_3 = db.Column(db.TEXT)
    shipping_price_3 = db.Column(db.DECIMAL(20, 2))
    shipping_day_least_3 = db.Column(db.INTEGER)
    shipping_day_most_3 = db.Column(db.INTEGER)

    not_shipping_1 = db.Column(db.INTEGER)
    not_shipping_2 = db.Column(db.INTEGER)
    not_shipping_3 = db.Column(db.INTEGER)
    not_shipping_4 = db.Column(db.INTEGER)
    not_shipping_5 = db.Column(db.INTEGER)
    not_shipping_6 = db.Column(db.INTEGER)

    currency = db.Column(db.INTEGER)
    digital_currency_1 = db.Column(db.INTEGER)
    digital_currency_2 = db.Column(db.INTEGER)
    digital_currency_3 = db.Column(db.INTEGER)

    # Category_Categories
    category_name_0 = db.Column(db.String(140))
    category_id_0 = db.Column(db.Integer)

    ad_item = db.Column(db.BOOLEAN)
    ad_item_level = db.Column(db.INTEGER)
    ad_item_timer = db.Column(db.TIMESTAMP())

    def __str__(self):
        return 'marketitem %s' % self.id

    def __repr__(self):
        return '<Auth_User %r>' % self.username


db.configure_mappers()
db.create_all()
db.session.commit()
