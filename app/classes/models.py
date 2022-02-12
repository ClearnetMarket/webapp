# coding=utf-8
from app import db


class Query_AdType(db.Model):
    __tablename__ = 'query_adtype'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_CategoryCats(db.Model):
    __tablename__ = 'query_word_list'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.VARCHAR(100))


class Query_Shard(db.Model):
    __tablename__ = 'query_shard'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_RequestCancel(db.Model):
    __tablename__ = 'query_requestcancel'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_RequestReturn(db.Model):
    __tablename__ = 'query_requestreturn'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_Return(db.Model):
    __tablename__ = 'query_return'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_Margin(db.Model):
    __tablename__ = 'query_margin'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(20, 8))
    text = db.Column(db.TEXT)


class Query_MainSearch(db.Model):
    __tablename__ = 'query_mainsearch'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_WebsiteFeedback(db.Model):
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


class Query_CurrencyList(db.Model):
    __tablename__ = 'query_currencylist'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_CountLow(db.Model):
    __tablename__ = 'query_count_low'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_PhysDig(db.Model):
    __tablename__ = 'query_physordig'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_ItemOrder(db.Model):
    __tablename__ = 'query_itemorder'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.TEXT)


class Query_ItemCount(db.Model):
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


class Query_ItemCondition(db.Model):
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


class Query_Currency(db.Model):
    __tablename__ = 'currency'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Integer)
    symbol = db.Column(db.TEXT)


class Query_Country(db.Model):
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
