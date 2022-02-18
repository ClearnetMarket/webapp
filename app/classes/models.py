# coding=utf-8
from app import db




class Query_AdType(db.Model):
    __tablename__ = 'query_adtype'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_CategoryCats(db.Model):
    __tablename__ = 'query_word_list'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.VARCHAR(100))


class Query_Shard(db.Model):
    __tablename__ = 'query_shard'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_RequestCancel(db.Model):
    __tablename__ = 'query_request_cancel'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_RequestReturn(db.Model):
    __tablename__ = 'query_request_return'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Return(db.Model):
    __tablename__ = 'query_return'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Margin(db.Model):
    __tablename__ = 'query_margin'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(20, 8))
    text = db.Column(db.VARCHAR(140))


class Query_MainSearch(db.Model):
    __tablename__ = 'query_main_search'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_WebsiteFeedback(db.Model):
    __tablename__ = 'query_website_feedback'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Carriers(db.Model):
    __tablename__ = 'query_carriers'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_CurrencyList(db.Model):
    __tablename__ = 'query_currency_list'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_CountLow(db.Model):
    __tablename__ = 'query_count_low'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_PhysDig(db.Model):
    __tablename__ = 'query_phys_or_dig'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_ItemOrder(db.Model):
    __tablename__ = 'query_item_order'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_ItemCount(db.Model):
    __tablename__ = 'query_item_count'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Timer(db.Model):
    __tablename__ = 'query_timer'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_ItemCondition(db.Model):
    __tablename__ = 'query_item_condition'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Continents(db.Model):
    __tablename__ = 'query_continents'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.INTEGER)
    text = db.Column(db.VARCHAR(140))


class Query_Currency(db.Model):
    __tablename__ = 'query_currency'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Integer)
    symbol = db.Column(db.VARCHAR(140))


class Query_Country(db.Model):
    __tablename__ = 'query_countries'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ab = db.Column(db.VARCHAR(10))
    name = db.Column(db.VARCHAR(140))
    numericcode = db.Column(db.INTEGER)


db.configure_mappers()
db.create_all()
db.session.commit()
