from app import db


class Checkout_CheckoutShoppingCart(db.Model):
    __tablename__ = 'checkout_shopping_cart'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    customer = db.Column(db.VARCHAR(40))
    customer_id = db.Column(db.INTEGER)
    vendor = db.Column(db.VARCHAR(40))
    vendor_id = db.Column(db.INTEGER)
    currency = db.Column(db.INTEGER)
    title_of_item = db.Column(db.VARCHAR(500))
    price_of_item = db.Column(db.DECIMAL(20, 2))
    string_auction_id = db.Column(db.VARCHAR(100))
    string_node_id = db.Column(db.VARCHAR(100))
    image_of_item = db.Column(db.VARCHAR(100))
    quantity_of_item = db.Column(db.INTEGER)
    return_policy = db.Column(db.TEXT)
    savedforlater = db.Column(db.INTEGER)
    item_id = db.Column(db.INTEGER)
    vendorsupply = db.Column(db.INTEGER)
    shipping_info_0 = db.Column(db.VARCHAR(350))
    shipping_day_least_0 = db.Column(db.INTEGER)
    shipping_day_most_0 = db.Column(db.INTEGER)
    shipping_info_2 = db.Column(db.VARCHAR(350))
    shipping_price_2 = db.Column(db.DECIMAL(20, 2))
    shipping_day_least_2 = db.Column(db.INTEGER)
    shipping_day_most_2 = db.Column(db.INTEGER)
    shipping_info_3 = db.Column(db.VARCHAR(350))
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
    selected_shipping_description = db.Column(db.VARCHAR(350))

    final_shipping_price_btc = db.Column(db.DECIMAL(20, 8))
    final_price_btc = db.Column(db.DECIMAL(20, 8))

    final_shipping_price_bch = db.Column(db.DECIMAL(20, 8))
    final_price_bch = db.Column(db.DECIMAL(20, 8))

    final_shipping_price_xmr = db.Column(db.DECIMAL(20, 8))
    final_price_xmr = db.Column(db.DECIMAL(20, 8))

class Checkout_ShoppingCartTotal(db.Model):
    __tablename__ = 'shoppingcarttotal'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    customer = db.Column(db.INTEGER)
    # btc
    btc_sumofitem = db.Column(db.INTEGER)
    btcprice = db.Column(db.DECIMAL(20, 8))
    shippingbtcprice = db.Column(db.DECIMAL(20, 8))
    totalbtcprice = db.Column(db.DECIMAL(20, 8))
    # bch
    btc_cash_sumofitem = db.Column(db.INTEGER)
    btc_cash_price = db.Column(db.DECIMAL(20, 8))
    shipping_btc_cashprice = db.Column(db.DECIMAL(20, 8))
    total_btc_cash_price = db.Column(db.DECIMAL(20, 8))
    # xmr
    xmr_sumofitem = db.Column(db.INTEGER)
    xmrprice = db.Column(db.DECIMAL(20, 12))
    shippingxmrprice = db.Column(db.DECIMAL(20, 12))
    totalxmrprice = db.Column(db.DECIMAL(20, 12))
    # affiliate stuff
    percent_off_order = db.Column(db.DECIMAL(6, 2))
    btc_cash_off = db.Column(db.DECIMAL(20, 8))
    btc_off = db.Column(db.DECIMAL(20, 8))
    xmr_off = db.Column(db.DECIMAL(20, 12))