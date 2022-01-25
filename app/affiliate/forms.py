from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length,  Regexp
from app.auth.validation import usernames


class AffiliateSignup(FlaskForm):

    username = StringField('Username', validators=[
        DataRequired(message='Vendor Signature is Required'),
        Length(1, 50),
        Regexp(usernames)])

    agreement = BooleanField(default=False)
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class AffiliateCode(FlaskForm):

    thecode = StringField(validators=[
        DataRequired(message='A code is required'),
        Length(5, 15),
        Regexp(usernames)])

    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False