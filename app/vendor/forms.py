from flask_wtf import FlaskForm

from wtforms import \
    StringField, \
    SubmitField, \
    TextAreaField, \
    SelectField, \
    BooleanField

from wtforms.validators import DataRequired, Length, Regexp, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.auth.validation import general
from app.common.query import sortbyrating


from app.classes.models import \
    Query_Carriers



class newOrders(FlaskForm):
    turnoff = BooleanField()
    submitcheckbox = SubmitField()


class acceptedOrders(FlaskForm):
    turnoff = BooleanField()
    submitcheckbox = SubmitField()




class vendorleavereview(FlaskForm):
    reviewcomment = StringField(validators=[
        DataRequired(message='Feedback message is Required'),
        Length(1, 250),
        Regexp(general)])
    submit = SubmitField()


class addShipping(FlaskForm):
    selectcarrier1 = QuerySelectField(query_factory=lambda: Query_Carriers.query.all(),
                                      get_label='text',
                                      )

    othercarrier1 = StringField(validators=[
        Optional(),
        Length(1, 250),
        Regexp(general)])
    trackingnumber1 = StringField(validators=[
        DataRequired(message='Tracking Number is required'),
        Length(5, 250),
        Regexp(general)])

    othercarrier2 = StringField(validators=[
        Optional(),
        Length(1, 250),
        Regexp(general)])

    trackingnumber2 = StringField(validators=[
        Optional(),
        Length(5, 250),
        Regexp(general)])

    selectcarrier2 = QuerySelectField(query_factory=lambda: Query_Carriers.query.all(),
                                      get_label='text')

    othercarrier3 = StringField(validators=[
        Optional(),
        Length(1, 250),
        Regexp(general)])
    trackingnumber3 = StringField(validators=[
        Optional(),
        Length(5, 250),
        Regexp(general)])

    selectcarrier3 = QuerySelectField(
        query_factory=lambda: Query_Carriers.query.all(), get_label='text')

    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class ratingsForm(FlaskForm):
    sortrating = SelectField(choices=sortbyrating())
    submit = SubmitField()


class feedbackcomment(FlaskForm):
    addreply = StringField(validators=[
        DataRequired(message='Feedback Comment is required'),
        Length(5, 150),
        Regexp(general)])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class markasrecieved(FlaskForm):
    submit = SubmitField()




class addtempreturn(FlaskForm):
    name = StringField(validators=[
        Optional(),
        Length(1, 450),
        Regexp(general)])
    street = StringField(validators=[
        Optional(),
        Length(1, 450),
        Regexp(general)])
    city = StringField(validators=[
        Optional(),
        Length(1, 450),
        Regexp(general)])
    state = StringField(validators=[
        Optional(),
        Length(1, 450),
        Regexp(general)])
    zip = StringField(validators=[
        Optional(),
        Length(1, 450),
        Regexp(general)])
    country = StringField(validators=[
        Optional(),
        Length(1, 450),
        Regexp(general)])
    messagereturn = TextAreaField(validators=[
        Optional(),
        Length(1, 2500),
    ])
    submit = SubmitField()
    cancelandrefund = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False
