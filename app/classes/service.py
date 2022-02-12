from app import db


class Service_ShippingSecret(db.Model):
    __tablename__ = 'shippingsecret'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    txtmsg = db.Column(db.TEXT)
    orderid = db.Column(db.INTEGER)


class Service_Returns(db.Model):
    __tablename__ = 'returns'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ordernumber = db.Column(db.INTEGER)
    name = db.Column(db.TEXT)
    street = db.Column(db.TEXT)
    city = db.Column(db.TEXT)
    state = db.Column(db.TEXT)
    country = db.Column(db.TEXT)
    zip = db.Column(db.TEXT)
    message = db.Column(db.TEXT)


class Service_DefaultReturns(db.Model):
    __tablename__ = 'defaultreturns'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.TEXT)
    street = db.Column(db.TEXT)
    city = db.Column(db.TEXT)
    state = db.Column(db.TEXT)
    country = db.Column(db.TEXT)
    zip = db.Column(db.TEXT)
    message = db.Column(db.TEXT)
    username = db.Column(db.TEXT)
    user_id = db.Column(db.INTEGER)


class Service_ReturnsTracking(db.Model):
    __tablename__ = 'returntracking'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ordernumber = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    customername = db.Column(db.TEXT)
    customerid = db.Column(db.INTEGER)
    vendorname = db.Column(db.TEXT)
    vendorid = db.Column(db.INTEGER)
    carrier = db.Column(db.INTEGER)
    trackingnumber = db.Column(db.TEXT)
    othercarrier = db.Column(db.TEXT)


class Service_Tracking(db.Model):
    __tablename__ = 'tracking'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.INTEGER)
    tracking1 = db.Column(db.TEXT)
    carrier1 = db.Column(db.TEXT)
    othercarrier1 = db.Column(db.TEXT)
    tracking2 = db.Column(db.TEXT)
    carrier2 = db.Column(db.TEXT)
    othercarrier2 = db.Column(db.TEXT)
    tracking3 = db.Column(db.TEXT)
    carrier3 = db.Column(db.TEXT)
    othercarrier3 = db.Column(db.TEXT)


class Service_UpdateLog(db.Model):
    __tablename__ = 'updatelog'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    header = db.Column(db.INTEGER)
    body = db.Column(db.INTEGER)
    dateofupdate = db.Column(db.TIMESTAMP())


class Service_CustomerServiceItem(db.Model):
    __tablename__ = 'customerserviceonitem'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue = db.Column(db.TEXT)


class Service_WebsiteFeedback(db.Model):
    __tablename__ = 'websitefeedback'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.TEXT)
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    comment = db.Column(db.TEXT)
    email = db.Column(db.TEXT)
    timestamp = db.Column(db.TIMESTAMP())


class Service_Issue(db.Model):
    __tablename__ = 'issues'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.TEXT)
    author_id = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())
    admin = db.Column(db.INTEGER)
    status = db.Column(db.INTEGER)


db.configure_mappers()
db.create_all()
db.session.commit()
