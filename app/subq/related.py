from app import db
from app.classes.item import marketItem


def relatedtoItem(id):
    item = db.session\
    .query(marketItem)\
    .filter_by(id=id)\
    .first()
    # category 5
    relatedcategory = db.session \
    .query(marketItem.itemtitlee,
            marketItem.stringauctionid,
            marketItem.stringnodeid,
            marketItem.id,
            marketItem.currency,
            marketItem.imageone,
            marketItem.price,
            marketItem.reviewcount,
            marketItem.itemrating,
            marketItem.digital_currency2,
            marketItem.digital_currency3,
            ) \
    .filter(marketItem.categoryid0 == item.categoryid0) \
    .filter(marketItem.online == 1) \
    .group_by(marketItem.id) \
    .limit(10)

    return relatedcategory


def itemsall():
    item = db.session.query(marketItem).limit(20)
    return item






