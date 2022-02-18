from app import db


class CategoryCats(db.Model):
    __tablename__ = 'category_cats'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True,
                   nullable=False)
    catid0 = db.Column(db.Integer)
    catname0 = db.Column(db.VARCHAR(300))
    formname = db.Column(db.VARCHAR(300))


class Category_Categories(db.Model):
    __tablename__ = 'category_categories'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=False)
    cat_id = db.Column(db.VARCHAR(300))
    name = db.Column(db.VARCHAR(300))
    cat_icon = db.Column(db.VARCHAR(30))




db.configure_mappers()
db.create_all()
db.session.commit()
