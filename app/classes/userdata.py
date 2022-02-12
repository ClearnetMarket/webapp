from app import db


class User_DataHistory(db.Model):
    __tablename__ = 'userhistory'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    recentcat1 = db.Column(db.INTEGER)
    recentcat1date = db.Column(db.TIMESTAMP())
    recentcat2 = db.Column(db.INTEGER)
    recentcat2date = db.Column(db.TIMESTAMP())
    recentcat3 = db.Column(db.INTEGER)
    recentcat3date = db.Column(db.TIMESTAMP())
    recentcat4 = db.Column(db.INTEGER)
    recentcat4date = db.Column(db.TIMESTAMP())
    recentcat5 = db.Column(db.INTEGER)
    recentcat5date = db.Column(db.TIMESTAMP())


class User_DataFeedback(db.Model):
    __tablename__ = 'feedback'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customername = db.Column(db.TEXT)
    sale_id = db.Column(db.INTEGER)
    vendorname = db.Column(db.TEXT)
    vendorid = db.Column(db.INTEGER)
    comment = db.Column(db.TEXT)
    item_rating = db.Column(db.INTEGER)
    item_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    vendorrating = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    addedtodb = db.Column(db.INTEGER)
    author_id = db.Column(db.INTEGER)


db.configure_mappers()
db.create_all()
db.session.commit()
