from app import db


class Userreviews(db.Model):
    __tablename__ = 'userreviews'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer = db.Column(db.TEXT)
    order_id = db.Column(db.INTEGER)
    customer_id = db.Column(db.INTEGER)
    review = db.Column(db.TEXT)
    dateofreview = db.Column(db.TIMESTAMP())
    rating = db.Column(db.INTEGER)


class Feedbackcomments(db.Model):
    __tablename__ = 'feedbackcomments'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP())
    author_id = db.Column(db.Integer)
    feedback_id = db.Column(db.Integer)
    sale_id = db.Column(db.Integer)


class exptable(db.Model):
    __tablename__ = 'exptable'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    user_id = db.Column(db.INTEGER)
    type = db.Column(db.INTEGER)
    amount = db.Column(db.INTEGER)
    timestamp = db.Column(db.TIMESTAMP())


class StatisticsVendor(db.Model):
    __tablename__ = 'statsvendor'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    username = db.Column(db.Text)
    vendorid = db.Column(db.INTEGER)
    totalsales = db.Column(db.INTEGER)
    totaltrades = db.Column(db.INTEGER)
    totalreviews = db.Column(db.INTEGER)
    startedselling = db.Column(db.TIMESTAMP())
    vendorrating = db.Column(db.DECIMAL(4, 2))
    avgitemrating = db.Column(db.DECIMAL(4, 2))
    diffpartners = db.Column(db.INTEGER)
    disputecount = db.Column(db.INTEGER)
    beenflagged = db.Column(db.INTEGER)
    totalbtcspent = db.Column(db.DECIMAL(20, 8))
    totalbtcrecieved = db.Column(db.DECIMAL(20, 8))
    totalbtccashspent = db.Column(db.DECIMAL(20, 8))
    totalbtccashrecieved = db.Column(db.DECIMAL(20, 8))
    totalusdmade = db.Column(db.DECIMAL(20, 2))


class StatisticsUser(db.Model):
    __tablename__ = 'statsuserr'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    username = db.Column(db.VARCHAR(50))
    user_id = db.Column(db.INTEGER)
    totalitemsbought = db.Column(db.INTEGER)
    totaltrades = db.Column(db.INTEGER)
    totalreviews = db.Column(db.INTEGER)
    startedbuying = db.Column(db.TIMESTAMP())
    diffpartners = db.Column(db.INTEGER)
    totalachievements = db.Column(db.INTEGER)
    userrating = db.Column(db.DECIMAL(4, 2))
    disputecount = db.Column(db.INTEGER)
    itemsflagged = db.Column(db.INTEGER)
    totalbtcspent = db.Column(db.DECIMAL(20, 8))
    totalbtcrecieved = db.Column(db.DECIMAL(20, 8))
    totalbtccashspent = db.Column(db.DECIMAL(20, 8))
    totalbtccashrecieved = db.Column(db.DECIMAL(20, 8))
    totalusdspent = db.Column(db.DECIMAL(20, 2))


db.configure_mappers()
db.create_all()
db.session.commit()
