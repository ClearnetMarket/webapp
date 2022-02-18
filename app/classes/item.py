from app import db


class Item_ItemtoDelete(db.Model):
    __tablename__ = 'item_to_delete'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True,
                   nullable=False)
    itemid = db.Column(db.Integer)



class Item_MarketItem(db.Model):
    __tablename__ = 'item_market_item'
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
    string_auction_id = db.Column(db.VARCHAR(40))
    string_node_id = db.Column(db.VARCHAR(40))

    origin_country = db.Column(db.INTEGER)
    destination_country_one = db.Column(db.INTEGER)
    destination_country_two = db.Column(db.INTEGER)
    destination_country_three = db.Column(db.INTEGER)
    destination_country_four = db.Column(db.INTEGER)
    destination_country_five = db.Column(db.INTEGER)

    item_title = db.Column(db.VARCHAR(500))
    item_count = db.Column(db.INTEGER)
    item_description = db.Column(db.TEXT)
    keywords = db.Column(db.VARCHAR(300))
    item_condition = db.Column(db.INTEGER)

    item_refund_policy = db.Column(db.TEXT)
    return_allowed = db.Column(db.INTEGER)

    image_one = db.Column(db.VARCHAR(100))
    image_two = db.Column(db.VARCHAR(100))
    image_three = db.Column(db.VARCHAR(100))
    image_four = db.Column(db.VARCHAR(100))
    image_five = db.Column(db.VARCHAR(100))

    details = db.Column(db.BOOLEAN)
    details_1 = db.Column(db.VARCHAR(500))
    details_1_answer = db.Column(db.VARCHAR(500))
    details_2 = db.Column(db.VARCHAR(500))
    details_2_answer = db.Column(db.VARCHAR(500))
    details_3 = db.Column(db.VARCHAR(500))
    details_3_answer = db.Column(db.VARCHAR(500))
    details_4 = db.Column(db.VARCHAR(500))
    details_4_answer = db.Column(db.VARCHAR(500))
    details_5 = db.Column(db.VARCHAR(500))
    details_5_answer = db.Column(db.VARCHAR(500))

    view_count = db.Column(db.INTEGER)
    item_rating = db.Column(db.DECIMAL(20, 2))
    review_count = db.Column(db.INTEGER)
    total_sold = db.Column(db.INTEGER)

    shipping_free = db.Column(db.BOOLEAN)
    shipping_two = db.Column(db.BOOLEAN)
    shipping_three = db.Column(db.BOOLEAN)

    shipping_info_0 = db.Column(db.VARCHAR(500))
    shipping_day_least_0 = db.Column(db.INTEGER)
    shipping_day_most_0 = db.Column(db.INTEGER)
    shipping_info_2 = db.Column(db.VARCHAR(500))
    shipping_price_2 = db.Column(db.DECIMAL(20, 2))
    shipping_day_least_2 = db.Column(db.INTEGER)
    shipping_day_most_2 = db.Column(db.INTEGER)
    shipping_info_3 = db.Column(db.VARCHAR(500))
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
    category_name_0 = db.Column(db.VARCHAR(140))
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
