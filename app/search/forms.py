from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import Length, Optional
from app.classes.models import Query_Country
from app.classes.category import Category_Categories

def searchside():
    return Category_Categories.query.filter(Category_Categories.id != 1000, Category_Categories.id != 100).order_by(Category_Categories.id.asc()).all()


def searchside_default():
    return Category_Categories.query.filter(Category_Categories.id == 1).first()


class searchForm(FlaskForm):
    # search name
    searchString = StringField(validators=[
        Optional(),
        Length(1, 250)])
    category = QuerySelectField(query_factory=searchside,
                                get_label='name',
                                default=searchside_default)

    # payment methods
    btccash = BooleanField(validators=[Optional()])
    btc = BooleanField(validators=[Optional()])

    # Pricing
    pricelow = IntegerField(Optional())
    pricehigh = IntegerField(Optional())

    # Shipping
    freeshipping = BooleanField(validators=[Optional()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False


class sortResults(FlaskForm):

    sortCategory = SelectField(
        choices=[('0', 'Most Relevant'),
                 ('1', 'Price: Highest First'),
                 ('2', 'Price: Lowest First'),
                 ('3', 'Top Items')
                 ]
    )

    destination_country_one = QuerySelectField(query_factory=lambda: Query_Country.query.all(),
                                               get_label='name',
                                               validators=[Optional()])
    # payment methods
    btccash = BooleanField(validators=[Optional()])
    btc = BooleanField(validators=[Optional()])

    # Pricing
    pricelow = IntegerField(Optional())
    pricehigh = IntegerField(Optional())

    # Shipping
    freeshipping = BooleanField(validators=[Optional()])

    sort = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):

        rv = FlaskForm.validate(self)
        if rv:
            return True
        else:
            return False
