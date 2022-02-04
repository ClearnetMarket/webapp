from flask_wtf import FlaskForm
from wtforms import StringField,\
    PasswordField,\
    SubmitField, \
    TextAreaField, \
    FileField,\
    BooleanField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,\
    Length,\
    Regexp,\
    EqualTo,\
    Optional
from app.classes.auth import User
from app.classes.models import Currency,\
    Query_mainsearch,\
    Query_Carriers,\
    Query_requestreturn,\
    Country
from flask import flash
from sqlalchemy import func
from flask_wtf.file import FileAllowed
from app.auth.validation import general,\
    onlynumbers,\
    usernames
import re
from app.auth.validation import allowspace
from app.classes.models import Categories, Country

class ConfirmSeed(FlaskForm):
    seedanswer0 = StringField('Word 1', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer1 = StringField('Word 2', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer2 = StringField('Word 3', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer3 = StringField('Word 4', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer4 = StringField('Word 5', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer5 = StringField('Word 6', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
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


class vendorSignup(FlaskForm):
    country = QuerySelectField(query_factory=lambda: Country.query.all(),
                               get_label='name',
                               validators=[DataRequired(message='Country is Required')])

    username = StringField('Username', validators=[
        DataRequired(message='Vendor Signature is Required'),
        Length(1, 50),
        Regexp(general)])

    agreement = BooleanField(default=False)
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class achselectForm(FlaskForm):
    ach1 = StringField(validators=[Optional(),
                                   Regexp(general),
                                   Length(2, 2)])
    ach2 = StringField(validators=[Optional(),
                                   Regexp(general),
                                   Length(2, 2)])
    ach3 = StringField(validators=[Optional(),
                                   Regexp(general),
                                   Length(2, 2)])
    ach4 = StringField(validators=[Optional(),
                                   Regexp(general),
                                   Length(2, 2)])
    ach5 = StringField(validators=[Optional(),
                                   Regexp(general),
                                   Length(2, 2)])
    selectone = SubmitField()
    deleteone = SubmitField()

    selecttwo = SubmitField()
    deletetwo = SubmitField()

    selectthree = SubmitField()
    deletethree = SubmitField()

    selectfour = SubmitField()
    deletefour = SubmitField()

    selectfive = SubmitField()
    deletefive = SubmitField()


class shipselectForm(FlaskForm):
    primary = SubmitField()
    delete = SubmitField()


def searchside():
    return Categories.query.filter(Categories.id != 1000, Categories.id != 100).order_by(Categories.id.asc()).all()


def searchside_default():
    return Categories.query.filter(Categories.id == 1).first()

class searchForm(FlaskForm):

    searchString = StringField('searchString', validators=[DataRequired()])
    category = QuerySelectField(query_factory=searchside,
                                get_label='name',
                                default=searchside_default)
    search = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        if len(self.searchString.data) < 1:
            return False

        # regex
        if re.search(allowspace, self.searchString.data):
            return True
        else:
            return False


class LoginForm(FlaskForm):
    username = StringField(validators=[
        DataRequired(),
        Length(3, 18),
        Regexp(usernames,
               message='Usernames must have only letters, numbers, dots or underscores')
    ])
    password_hash = PasswordField(validators=[
        DataRequired(),
        Length(7, 128),
        Regexp(general),
    ])

    submit = SubmitField('')

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class RegistrationForm(FlaskForm):
    username = StringField(validators=[
        DataRequired(),
        Length(3, 18),
        Regexp(usernames,
               message='Usernames must have only letters, numbers, dots or underscores')
    ])

    promocode = StringField(validators=[
        Length(5, 15),
        Optional(),
    ])
    password = PasswordField(validators=[
        DataRequired(),
        Length(7, 128),
        Regexp(general),
        EqualTo('passwordtwo',
                message='Passwords must match.')
    ])
    passwordtwo = PasswordField(validators=[
        DataRequired(),
        Regexp(general),
    ])
    country = QuerySelectField(query_factory=lambda: Country.query.order_by(Country.name.asc()).all(),
                               get_label='name',
                               validators=[
        DataRequired()
    ])
    currency = QuerySelectField(query_factory=lambda: Currency.query.order_by(Currency.symbol.asc()).all(),
                                get_label='symbol',
                                validators=[
        DataRequired()
    ])
    walletpin = PasswordField(validators=[
        DataRequired(),
        Length(4, 4),
        Regexp(onlynumbers),
        EqualTo('walletpintwo',
                message='Pin must match.  Pin must be 4 digits,  No letters/symbols')
    ])
    walletpintwo = PasswordField(validators=[DataRequired(),
                                             Regexp(onlynumbers),
                                             ])

    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        rv = FlaskForm.validate(self)
        if rv is True:
            username = User.query.filter(func.lower(User.username) == func.lower(self.username.data)).first()
            if username:

                flash('Username is already taken', category="success")
                return False

            else:
                return True



class CheckSeed(FlaskForm):
    """
    Used for changing seed/recovering account
    """
    username = StringField(validators=[
        DataRequired(),
        Length(3, 18),
        Regexp(usernames,
               message='Usernames must have only letters, numbers, dots or underscores')
    ])
    seedanswer0 = StringField('Word 1', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer1 = StringField('Word 2', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer2 = StringField('Word 3', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer3 = StringField('Word 4', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer4 = StringField('Word 5', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer5 = StringField('Word 6', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
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


class ChangePasswordForm(FlaskForm):
    """
    changes the password
    """

    newpassword = PasswordField('New password', validators=[
        DataRequired(),
        Regexp(general),
        Length(7, 64),
        EqualTo('newpasswordtwo',
                message='Passwords must match')
    ])
    newpasswordtwo = PasswordField('Confirm new password', validators=[
        DataRequired(),
        Regexp(general),
    ])

    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):
        rv = FlaskForm.validate(self)
        if rv is True:
            return True
        else:
            return False


class ChangePinForm(FlaskForm):

    newpin1 = PasswordField('New Four Digit Pin', validators=[
        DataRequired(),
        Length(4, 4),
        Regexp(onlynumbers),
        EqualTo('newpin2',
                message='Pins must match. Pin is 4 digits long')
    ])
    newpin2 = PasswordField('Confirm new pin', validators=[
        DataRequired(),
        Regexp(onlynumbers),
    ])

    submit = SubmitField('Update Pin')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class VacationForm(FlaskForm):

    Vacation = SubmitField('')


def myaccount_form_factory(user):
    class myAccountForm(FlaskForm):

        Bio = TextAreaField(validators=[
            Optional(),
            Length(10, 3500),
            Regexp(general, message="No Special characters allowed"),

        ])

        origincountry1 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                          get_label='name',
                                          default=lambda: Country.query.filter_by(numericcode=user.country).first(),
                                          validators=[DataRequired(message='Your Country is required')])

        currency1 = QuerySelectField(query_factory=lambda: Currency.query.all(),
                                     default=lambda: Currency.query.filter_by(code=user.currency).first(),
                                     get_label='symbol',
                                     validators=[DataRequired(message='Your Currency is required')])

        imageprofile = FileField(validators=[Optional(),
                                             FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'], 'Images only')
                                             ])

        submit = SubmitField()

        delete = SubmitField()

        def __init__(self, *args, **kwargs):
            FlaskForm.__init__(self, *args, **kwargs)

        def validate(self, *args, **kwargs):

            rv = FlaskForm.validate(self)

            if rv:
                return True
            else:
                return False

    return myAccountForm


class becomeavendor(FlaskForm):

    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class feedbackonorderForm(FlaskForm):

    feedbacktext = StringField(validators=[
        DataRequired(message='Review must be 5-140 characters long'),
        Length(1, 100),
        Regexp(general)

    ])

    submitfeedback = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class requestCancelform(FlaskForm):

    type = QuerySelectField(query_factory=lambda: Query_requestreturn.query.all(),
                            get_label='text',

                            validators=[DataRequired(message='Category Required')])

    messagewhy = TextAreaField(validators=[
        DataRequired(),
        Length(10, 1000),
        Regexp(general)
    ])

    submit = SubmitField()


    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class markasSent(FlaskForm):

    othercarrier = StringField(validators=[Optional(),
                                           Regexp(general),
                                           Length(5, 50)])
    trackingnumber = StringField(validators=[DataRequired(),
                                             Regexp(general),
                                             Length(5, 75)])

    carrier = QuerySelectField(query_factory=lambda: Query_Carriers.query.all(),
                               get_label='text',
                               )
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class returnitemconfirm(FlaskForm):
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


def returnitem_form_factory(orderid):
    class requestReturn(FlaskForm):

        type = QuerySelectField(query_factory=lambda: (Query_requestreturn).query.all(),
                                get_label='text',
                                validators=[DataRequired(message='Category Required')])

        messagewhy = TextAreaField(validators=[
            DataRequired(message='Message Required'),
            Length(1, 500),
            Regexp(general)

        ])

        submit = SubmitField()

        def __init__(self, *args, **kwargs):
            FlaskForm.__init__(self, *args, **kwargs)

        def validate(self, *args, **kwargs):

            rv = FlaskForm.validate(self)
            if rv:
                return True
            else:
                return False
    return requestReturn


class Deleteaccountform(FlaskForm):

    seedanswer0 = StringField('Word 1', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer1 = StringField('Word 2', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer2 = StringField('Word 3', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer3 = StringField('Word 4', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer4 = StringField('Word 5', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
        Regexp(general)])
    seedanswer5 = StringField('Word 6', validators=[
        DataRequired(message='Word is Required'),
        Length(1, 50),
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