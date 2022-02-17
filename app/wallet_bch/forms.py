from flask_wtf import\
    FlaskForm
from wtforms import\
    StringField,\
    PasswordField,\
    SubmitField
from wtforms.validators import\
    DataRequired,\
    Length,\
    Regexp,\
    Optional
from app.auth.validation import\
    btcamount,\
    general,\
    onlynumbers


class BchWalletSendCoin(FlaskForm):
    sendto = StringField(validators=[DataRequired(),
                                     Length(54, 54),

                                     ])

    description = StringField(validators=[Optional(),
                                          Length(2, 100),
                                          Regexp(general)
                                          ])

    amount = StringField(validators=[DataRequired(),
                                     Length(1, 11),
                                     Regexp(btcamount)
                                     ])
    pin = PasswordField(validators=[
        DataRequired(),
        Regexp(onlynumbers),
        Length(4, 4),
    ])


    submit = SubmitField('')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):

        rv = FlaskForm.validate(self)

        if rv:
            return True
        else:
            return False
