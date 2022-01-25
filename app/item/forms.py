from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import Regexp, Length, DataRequired, optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.auth.validation import general
from app.classes.models import Query_Currencylist
from app.auth.validation import usernames


class flagListing(FlaskForm):
    banit = SubmitField()
    flagit = SubmitField()


class additemForm(FlaskForm):

    addtocart1 = SubmitField()
    save = SubmitField()


class shoppingcartForm(FlaskForm):

    saveforlater = SubmitField()
    update = SubmitField()
    delete = SubmitField()
    gotocheckout = SubmitField()

    currency_selection = QuerySelectField(query_factory=lambda: Query_Currencylist.query.all(),
                                          get_label='text',
                                          validators=[DataRequired(message='Currency is required')])


class checkoutForm(FlaskForm):

    MakePayment = SubmitField()


class changeShipping(FlaskForm):

    updateShipping = SubmitField()


class promoandgiftform(FlaskForm):

    promocode = StringField(validators=[
        optional(),
        Length(5, 15),
        Regexp(usernames)
                       ])
    addpromo = SubmitField()

    def validate(self):

        rv = FlaskForm.validate(self)

        if rv:
            return True
        else:
            return False


class custominfo(FlaskForm):

    privatemsg = TextAreaField(validators=[DataRequired(),
                                           Regexp(general, message="No Special characters allowed"),
                                           Length(1, 3500)])

    custommsgbtn = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):

        rv = FlaskForm.validate(self)

        if rv:
            return True
        else:
            return False


class custominfoDelete(FlaskForm):

    deletemsgbtn = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):

        rv = FlaskForm.validate(self)

        if rv:
            return True
        else:
            return False

