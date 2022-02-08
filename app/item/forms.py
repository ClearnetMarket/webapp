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

