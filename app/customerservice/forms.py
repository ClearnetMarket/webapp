from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Regexp
from app.common.query import feedbacklist
from app.classes.service import Service_CustomerServiceItem
from wtforms_sqlalchemy.fields import QuerySelectField
from flask import flash
from app.auth.validation import general


class issuewithItem(FlaskForm):
    issuebody = TextAreaField(validators=[DataRequired(),
                                          Regexp(general),
                                          Length(1, 250)
                                          ])
    subject = QuerySelectField(
        query_factory=lambda: Service_CustomerServiceItem.query.all(), get_label='issue')
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
        Length(5, 100),
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


class Chatform(FlaskForm):

    bodyofchat = TextAreaField(validators=[
        DataRequired(),
        Length(1, 64),
    ])
    post = SubmitField()


class adminhelpserviceform(FlaskForm):
    resolved = SubmitField()
    becomeadmin = SubmitField()
    delete = SubmitField()


class Feedback(FlaskForm):
    type = SelectField('Feedback Type', choices=feedbacklist(),
                       validators=[DataRequired()])
    message2 = TextAreaField('Message', validators=[DataRequired(),
                                                    Regexp(general),
                                                    Length(1, 150), ])

    recaptchaanswer = StringField(validators=[DataRequired()])

    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):
        if 1 < len(self.message2.data) <= 2500:
            return True
        else:
            flash("Message needed")
            return False


class sendmessageForm(FlaskForm):
    body1 = TextAreaField(validators=[DataRequired(message='Body is Required'),
                                      Length(1, 2500),
                                      Regexp(general)
                                      ])

    recaptchaanswer = StringField('', validators=[
        DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False
