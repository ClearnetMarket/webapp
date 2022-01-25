from wtforms import Form, StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, Optional
from app.auth.validation import general, onlynumbers, usernames, bitcoin
from flask_wtf import FlaskForm


class topbuttonForm(FlaskForm):

    delete = SubmitField()
    markasread = SubmitField()


class PostForm(FlaskForm):
    body = TextAreaField(validators=[DataRequired(),
                                     Length(1, 2500),
                                     Regexp(general)
                                         ])


    submit = SubmitField()



class CommentForm(FlaskForm):
    msgplace = TextAreaField(validators=[DataRequired(message='Comment Required'),
                                      Length(1,2500),
                                      Regexp(general)
                                      ])
    submit1 = SubmitField()
    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class addusertoconvoForm(FlaskForm):
    adduserbody = StringField( validators=[DataRequired(message='Username Required'),
                                    Length(1, 50),
                                    Regexp(usernames)
                                    ])
    submit2 = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False

class sendmessageForm(FlaskForm):
    subject = StringField(validators=[DataRequired(message='Subject is required'),
                                     Length(1,150),
                                      Regexp(general)

                                                 ])
    username = StringField(validators=[Optional(),
                                                  Regexp(usernames)
                                                  ])
    body1 = TextAreaField(validators=[DataRequired(message='Body is Required'),
                                     Regexp(general),
                                     Length(1, 2500)
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


class allActionForm(FlaskForm):
    submit = SubmitField()


