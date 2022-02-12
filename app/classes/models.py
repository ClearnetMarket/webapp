# coding=utf-8
from app import db


class QueryAdType(db.Model):
    __tablename__ = 'query_adtype'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class WordSeeds(db.Model):
    __tablename__ = 'query_word_list'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.VARCHAR(100))


class Categories(db.Model):
    __tablename__ = 'category'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    name = db.Column(db.TEXT)


class Cats(db.Model):
    __tablename__ = 'cats'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True, nullable=False)
    catid0 = db.Column(db.INTEGER, db.ForeignKey(
        'marketitem.category_id_0', name="fk_cat5"), nullable=False)
    catname0 = db.Column(db.TEXT)
    catid1 = db.Column(db.INTEGER, db.ForeignKey(
        'marketitem.categoryid1', name="fk_cat5"), nullable=False)
    catname1 = db.Column(db.TEXT)
    catid2 = db.Column(db.INTEGER, db.ForeignKey(
        'marketitem.categoryid2', name="fk_cat5"), nullable=False)
    catname2 = db.Column(db.TEXT)
    catid3 = db.Column(db.INTEGER, db.ForeignKey(
        'marketitem.categoryid3', name="fk_cat5"), nullable=False)
    catname3 = db.Column(db.TEXT)
    catid4 = db.Column(db.INTEGER, db.ForeignKey(
        'marketitem.categoryid4', name="fk_cat5"), nullable=False)
    catname4 = db.Column(db.TEXT)
    catid5 = db.Column(db.INTEGER, db.ForeignKey(
        'marketitem.categoryid5', name="fk_cat5"), nullable=False)
    catname5 = db.Column(db.TEXT)
    formname = db.Column(db.TEXT)


class btc_cash_Prices(db.Model):
    __tablename__ = 'prices_btc_cash'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency = db.Column(db.TEXT)
    price = db.Column(db.DECIMAL(50, 2))
    currency_id = db.Column(db.INTEGER)
    percent_change_twentyfour = db.Column(db.DECIMAL(50, 2))


class Query_shard(db.Model):
    __tablename__ = 'query_shard'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_requestcancel(db.Model):
    __tablename__ = 'query_requestcancel'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_requestreturn(db.Model):
    __tablename__ = 'query_requestreturn'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_return(db.Model):
    __tablename__ = 'query_return'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_margin(db.Model):
    __tablename__ = 'query_margin'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(20, 8))
    text = db.Column(db.TEXT)


class Query_mainsearch(db.Model):
    __tablename__ = 'query_mainsearch'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_websitefeedback(db.Model):
    __tablename__ = 'query_websitefeedback'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_Carriers(db.Model):
    __tablename__ = 'query_carriers'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_Currencylist(db.Model):
    __tablename__ = 'query_currencylist'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_Count_low(db.Model):
    __tablename__ = 'query_count_low'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_Physordig(db.Model):
    __tablename__ = 'query_physordig'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_Itemorder(db.Model):
    __tablename__ = 'query_itemorder'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_item_count(db.Model):
    __tablename__ = 'query_item_count'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_Timer(db.Model):
    __tablename__ = 'query_timer'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_item_condition(db.Model):
    __tablename__ = 'query_item_condition'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_Continents(db.Model):
    __tablename__ = 'query_continents'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Currency(db.Model):
    __tablename__ = 'currency'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Integer)
    symbol = db.Column(db.TEXT)


class Country(db.Model):
    __tablename__ = 'countries'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ab = db.Column(db.TEXT)
    name = db.Column(db.TEXT)
    numericcode = db.Column(db.INTEGER)


db.configure_mappers()
db.create_all()
db.session.commit()
