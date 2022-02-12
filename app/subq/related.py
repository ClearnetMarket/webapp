from app import db
from app.classes.item import marketitem


def relatedtoItem(id):
    item = db.session\
        .query(marketitem)\
        .filter_by(id=id)\
        .first()
    # category 5
    relatedcategory = db.session \
        .query(marketitem.item_title,
               marketitem.string_auction_id,
               marketitem.string_node_id,
               marketitem.id,
               marketitem.currency,
               marketitem.image_one,
               marketitem.price,
               marketitem.review_count,
               marketitem.item_rating,
               marketitem.digital_currency_2,
               marketitem.digital_currency_3,
               ) \
        .filter(marketitem.category_id_0 == item.category_id_0) \
        .filter(marketitem.online == 1) \
        .group_by(marketitem.id) \
        .limit(10)

    return relatedcategory


def itemsall():
    item = db.session.query(marketitem).limit(20)
    return item
