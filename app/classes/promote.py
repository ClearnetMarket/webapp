from app import db


class PromotedItem(db.Model):
    __tablename__ = 'category'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    itemid = db.Column(db.INTEGER)


db.configure_mappers()
db.create_all()
db.session.commit()
