from app import db
from app.classes.item import Item_MarketItem


def subq_related_to_item(id):
    item = db.session\
        .query(Item_MarketItem)\
        .filter_by(id=id)\
        .first()
    # category 5
    relatedcategory = db.session \
        .query(Item_MarketItem.item_title,
               Item_MarketItem.string_auction_id,
               Item_MarketItem.string_node_id,
               Item_MarketItem.id,
               Item_MarketItem.currency,
               Item_MarketItem.image_one,
               Item_MarketItem.price,
               Item_MarketItem.review_count,
               Item_MarketItem.item_rating,
               Item_MarketItem.digital_currency_2,
               Item_MarketItem.digital_currency_3,
               ) \
        .filter(Item_MarketItem.category_id_0 == item.category_id_0) \
        .filter(Item_MarketItem.online == 1) \
        .group_by(Item_MarketItem.id) \
        .limit(10)

    return relatedcategory


def itemsall():
    item = db.session.query(Item_MarketItem).limit(20)
    return item
