from app import db


class whichAch(db.Model):
    __tablename__ = 'whichAch'
    __bind_key__ = 'clearnet_Market_Users'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    userid = db.Column(db.INTEGER)
    ach1 = db.Column(db.TEXT)
    ach2 = db.Column(db.TEXT)
    ach3 = db.Column(db.TEXT)
    ach4 = db.Column(db.TEXT)
    ach5 = db.Column(db.TEXT)

    ach1_cat = db.Column(db.TEXT)
    ach2_cat = db.Column(db.TEXT)
    ach3_cat = db.Column(db.TEXT)
    ach4_cat = db.Column(db.TEXT)
    ach5_cat = db.Column(db.TEXT)


class UserAchievements_recent(db.Model):
    __tablename__ = 'userachievements_recent'
    __bind_key__ = 'clearnet_Market_Users'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    userid = db.Column(db.INTEGER)
    username = db.Column(db.Text)

    ach_id = db.Column(db.INTEGER)
    achievement_date = db.Column(db.TIMESTAMP())
    viewed = db.Column(db.INTEGER)


class UserAchievements(db.Model):
    __tablename__ = 'userachievements'
    __bind_key__ = 'clearnet_Market_Users'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True,  unique=True)
    userid = db.Column(db.INTEGER)
    username = db.Column(db.Text)
    experiencepoints = db.Column(db.INTEGER)
    level = db.Column(db.INTEGER)

    a1 = db.Column(db.INTEGER)
    a1_date = db.Column(db.TIMESTAMP())
    a2 = db.Column(db.INTEGER)
    a2_date = db.Column(db.TIMESTAMP())
    a3 = db.Column(db.INTEGER)
    a3_date = db.Column(db.TIMESTAMP())
    a4 = db.Column(db.INTEGER)
    a4_date = db.Column(db.TIMESTAMP())
    a5 = db.Column(db.INTEGER)
    a5_date = db.Column(db.TIMESTAMP())
    a6 = db.Column(db.INTEGER)
    a6_date = db.Column(db.TIMESTAMP())
    a7 = db.Column(db.INTEGER)
    a7_date = db.Column(db.TIMESTAMP())
    a8 = db.Column(db.INTEGER)
    a8_date = db.Column(db.TIMESTAMP())
    a9 = db.Column(db.INTEGER)
    a9_date = db.Column(db.TIMESTAMP())

    # exp levels
    e1 = db.Column(db.INTEGER)
    e1_date = db.Column(db.TIMESTAMP())
    e2 = db.Column(db.INTEGER)
    e2_date = db.Column(db.TIMESTAMP())
    e3 = db.Column(db.INTEGER)
    e3_date = db.Column(db.TIMESTAMP())
    e4 = db.Column(db.INTEGER)
    e4_date = db.Column(db.TIMESTAMP())
    e5 = db.Column(db.INTEGER)
    e5_date = db.Column(db.TIMESTAMP())
    e6 = db.Column(db.INTEGER)
    e6_date = db.Column(db.TIMESTAMP())
    e7 = db.Column(db.INTEGER)
    e7_date = db.Column(db.TIMESTAMP())
    e8 = db.Column(db.INTEGER)
    e8_date = db.Column(db.TIMESTAMP())
    e9 = db.Column(db.INTEGER)
    e9_date = db.Column(db.TIMESTAMP())

    # vendor achievs
    v1 = db.Column(db.INTEGER)
    v1_date = db.Column(db.TIMESTAMP())
    v2 = db.Column(db.INTEGER)
    v2_date = db.Column(db.TIMESTAMP())
    v3 = db.Column(db.INTEGER)
    v3_date = db.Column(db.TIMESTAMP())
    v4 = db.Column(db.INTEGER)
    v4_date = db.Column(db.TIMESTAMP())
    v5 = db.Column(db.INTEGER)
    v5_date = db.Column(db.TIMESTAMP())
    v6 = db.Column(db.INTEGER)
    v6_date = db.Column(db.TIMESTAMP())
    v7 = db.Column(db.INTEGER)
    v7_date = db.Column(db.TIMESTAMP())
    v8 = db.Column(db.INTEGER)
    v8_date = db.Column(db.TIMESTAMP())
    v9 = db.Column(db.INTEGER)
    v9_date = db.Column(db.TIMESTAMP())
    v10 = db.Column(db.INTEGER)
    v10_date = db.Column(db.TIMESTAMP())
    v11 = db.Column(db.INTEGER)
    v11_date = db.Column(db.TIMESTAMP())
    v12 = db.Column(db.INTEGER)
    v12_date = db.Column(db.TIMESTAMP())
    v13 = db.Column(db.INTEGER)
    v13_date = db.Column(db.TIMESTAMP())
    v14 = db.Column(db.INTEGER)
    v14_date = db.Column(db.TIMESTAMP())
    v15 = db.Column(db.INTEGER)
    v15_date = db.Column(db.TIMESTAMP())
    v16 = db.Column(db.INTEGER)
    v16_date = db.Column(db.TIMESTAMP())

    # first to do something
    u1 = db.Column(db.INTEGER)
    u1_date = db.Column(db.TIMESTAMP())
    u2 = db.Column(db.INTEGER)
    u2_date = db.Column(db.TIMESTAMP())
    u3 = db.Column(db.INTEGER)
    u3_date = db.Column(db.TIMESTAMP())
    u4 = db.Column(db.INTEGER)
    u4_date = db.Column(db.TIMESTAMP())
    u5 = db.Column(db.INTEGER)
    u5_date = db.Column(db.TIMESTAMP())

    # customer achievs
    c1 = db.Column(db.INTEGER)
    c1_date = db.Column(db.TIMESTAMP())
    c2 = db.Column(db.INTEGER)
    c2_date = db.Column(db.TIMESTAMP())
    c3 = db.Column(db.INTEGER)
    c3_date = db.Column(db.TIMESTAMP())
    c4 = db.Column(db.INTEGER)
    c4_date = db.Column(db.TIMESTAMP())
    c5 = db.Column(db.INTEGER)
    c5_date = db.Column(db.TIMESTAMP())
    c6 = db.Column(db.INTEGER)
    c6_date = db.Column(db.TIMESTAMP())
    c7 = db.Column(db.INTEGER)
    c7_date = db.Column(db.TIMESTAMP())
    c8 = db.Column(db.INTEGER)
    c8_date = db.Column(db.TIMESTAMP())
    c9 = db.Column(db.INTEGER)
    c9_date = db.Column(db.TIMESTAMP())
    c10 = db.Column(db.INTEGER)
    c10_date = db.Column(db.TIMESTAMP())
    c11 = db.Column(db.INTEGER)
    c11_date = db.Column(db.TIMESTAMP())
    c12 = db.Column(db.INTEGER)
    c12_date = db.Column(db.TIMESTAMP())

    # bitcoin achievs
    b1 = db.Column(db.INTEGER)
    b1_date = db.Column(db.TIMESTAMP())
    b2 = db.Column(db.INTEGER)
    b2_date = db.Column(db.TIMESTAMP())
    b3 = db.Column(db.INTEGER)
    b3_date = db.Column(db.TIMESTAMP())
    b4 = db.Column(db.INTEGER)
    b4_date = db.Column(db.TIMESTAMP())
    b5 = db.Column(db.INTEGER)
    b5_date = db.Column(db.TIMESTAMP())


class Achievements(db.Model):
    __tablename__ = 'achievements'
    __bind_key__ = 'clearnet_Market_Users'
    __table_args__ = {"schema": "public", 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    categoryid = db.Column(db.TEXT)
    categoryname = db.Column(db.TEXT)
    value = db.Column(db.INTEGER)
    category = db.Column(db.INTEGER)
    title = db.Column(db.TEXT)
    description = db.Column(db.TEXT)
    dateadded = db.Column(db.TIMESTAMP())


db.configure_mappers()
db.create_all()
db.session.commit()
