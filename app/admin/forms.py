from flask_wtf import FlaskForm
from wtforms import\
    StringField,\
    SubmitField,\
    SelectField,\
    TextAreaField,\
    IntegerField, \
    DecimalField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from app.common.query import achievementcategory, achievementvalue, admin_role
from app.classes.models import Query_shard


class changeUserForm(FlaskForm):
    # vendor
    vendor_totalbtcrecieved = DecimalField()
    vendor_totalbtcspent = DecimalField()
    vendor_totalsales = IntegerField()
    vendor_totalreviews = IntegerField()
    vendor_totaltrades = IntegerField()
    vendor_vendorrating = DecimalField()
    vendor_itemrating = DecimalField()


    # customer
    customer_totalitemsbought = IntegerField()
    customer_totalreviews = IntegerField()
    customer_totaltrades = IntegerField()
    customer_totalbtcrecieved = DecimalField()
    customer_totalbtcspent = DecimalField()

    # both
    difftradingpartners = IntegerField()
    changeuser = SubmitField('')


class changeitemForm(FlaskForm):
    searchbar = StringField(validators=[
        DataRequired(),
        Length(1, 164)])
    comment = StringField(validators=[
        DataRequired(),
        Length(1, 164)])
    vendorrating = IntegerField()
    itemrating = IntegerField()
    finditem = SubmitField('')


class searchadminForm(FlaskForm):

    searchbar = StringField(validators=[
        DataRequired(),
        Length(1, 164)])
    changeuser_searchbar = StringField(validators=[
        DataRequired(),
        Length(1, 164)])

    change_usersearch = SubmitField('')
    finduser = SubmitField('')
    findorder = SubmitField('')
    finditem = SubmitField('')
    finddtrade = SubmitField('')
    findbtctrade = SubmitField('')


class addupdateform(FlaskForm):
    title = StringField(validators=[
        DataRequired(),
        Length(7, 64)])
    description = TextAreaField(validators=[
        DataRequired(),
        Length(7, 500)])
    submit = SubmitField('')


class addachievement(FlaskForm):
    achid = StringField()

    title = StringField(validators=[
        DataRequired(),
        Length(7, 64)])

    description = StringField('', validators=[
        DataRequired(),
        Length(7, 64)])

    category = SelectField(choices=achievementcategory(),
                           description="",
                           validators=[DataRequired()])
    value = SelectField(choices=achievementvalue(),
                        description="",
                        validators=[DataRequired()])
    submit = SubmitField('')


class settoAdmin(FlaskForm):
    username = StringField(validators=[
        DataRequired(),
        Length(7, 64)])

    admin_role = SelectField('',
                             choices=admin_role(),
                             description="",
                             validators=[DataRequired()])
    submit = SubmitField('')



class Chatform(FlaskForm):

    msgstufftosend = TextAreaField(validators=[
        DataRequired(),
        Length(1, 64),
    ])

    post = SubmitField()


class profitform(FlaskForm):
    balance = SubmitField()


class Disputeform(FlaskForm):

    start = SubmitField()
    one = SubmitField()
    two = SubmitField()
    three = SubmitField()
    four = SubmitField()
    five = SubmitField()
    undispute = SubmitField()
    addtime1 = SubmitField()
    addtimetwodays = SubmitField()
    addtimeweek = SubmitField()
    abortorder = SubmitField()


class Userform(FlaskForm):

    lockwallet = SubmitField()
    unlockwallet = SubmitField()
    selectshard = QuerySelectField(query_factory=lambda: Query_shard.query.all(), get_label='text')
    selectshardsubmit = SubmitField()


class adminsendMoney(FlaskForm):
    sendto = StringField()
    description = StringField()
    amount = StringField()
    submit = SubmitField('')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)

        if rv:
            return True
        else:
            return False