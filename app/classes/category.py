from app import db


class Categories(db.Model):
    __tablename__ = 'category'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=False)
    cat_id = db.Column(db.TEXT)
    name = db.Column(db.TEXT)
    cat_icon = db.Column(db.VARCHAR(30))

db.configure_mappers()
db.create_all()
db.session.commit()
