from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from wtforms import \
    StringField, \
    SubmitField, \
    TextAreaField, \
    BooleanField, \
    FileField, \
    DecimalField
from decimal import Decimal
from wtforms.validators import DataRequired, Length, Regexp, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.auth.validation import general

from app.classes.category import Category_Categories

from app.classes.models import \
    Query_Currency, \
    Query_CountLow, \
    Query_Continents, \
    Query_ItemCondition, \
    Query_ItemCount, \
    Query_Country


class UploadEbayForm(FlaskForm):
    ebaydata = FileField('CSV File', validators=[
        FileAllowed(['csv'],
                    DataRequired()
                    )
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


class deactive(FlaskForm):
    turnoff = BooleanField()
    submitcheckbox = SubmitField()


def add_product_form_factory(item):
    class vendorcreateItem(FlaskForm):
        btc_accepted = BooleanField(default=True)
        btc_cash_accepted = BooleanField(default=True)

        item_title = StringField(validators=[DataRequired(message="A title is required for your listing"),
                                             Length(1, 100),
                                             Regexp(general),
                                             ])

        item_refund_policy = TextAreaField(validators=[Optional(),
                                                       Regexp(general),
                                                       Length(1, 500),
                                                       ])

        price = DecimalField(validators=[DataRequired(message='Item Price is Required'),
                                         ])

        item_description = TextAreaField(validators=[
            DataRequired(message='Item Description is Required'),
            Regexp(general),
            Length(5, 1500)])

        details = BooleanField(default=False)

        details_1 = StringField(validators=[Optional(),
                                            Length(1, 50),
                                            Regexp(general)])

        details_1_answer = StringField(validators=[Optional(),
                                                   Length(1, 50),
                                                   Regexp(general)])

        details_2 = StringField(validators=[Optional(),
                                            Length(1, 50),
                                            Regexp(general)])
        details_2_answer = StringField(validators=[Optional(),
                                                   Length(1, 50),
                                                   Regexp(general)])

        details_3 = StringField(validators=[Optional(),
                                            Length(1, 50),
                                            Regexp(general)])

        details_3_answer = StringField(validators=[Optional(),
                                                   Length(1, 50),
                                                   Regexp(general)])

        details_4 = StringField(validators=[Optional(),
                                            Length(1, 50),
                                            Regexp(general)])

        details_4_answer = StringField(validators=[Optional(),
                                                   Length(1, 50),
                                                   Regexp(general)])

        details_5 = StringField(validators=[Optional(),
                                            Length(1, 50),
                                            Regexp(general)])

        details_5_answer = StringField(validators=[Optional(),
                                                   Length(1, 50),
                                                   Regexp(general)])

        image_one1 = FileField('Primary Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                        message='Images only or wrong format')
                                                            ])

        image_two = FileField('Upload Image 2', validators=[Optional(),
                                                            FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                        message='Images only or wrong format')
                                                            ])

        image_three = FileField('Upload Image 3', validators=[Optional(),
                                                              FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                          message='Images only or wrong format')
                                                              ])

        image_four = FileField('Upload Image 4', validators=[Optional(),
                                                             FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                         message='Images only or wrong format')
                                                             ])

        image_five = FileField('Upload Image 5', validators=[Optional(),
                                                             FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                         message='Images only or wrong format')
                                                             ])

        keywords = StringField(validators=[
            DataRequired(message='Keywords are the terms used to find your item in the search results.  '
                                 'They are required'),
            Length(5, 200),
            Regexp(general)])

        return_this_item = BooleanField(default=False)
        shipping_free = BooleanField(default=False)
        shipping_two = BooleanField(default=False)
        shipping_three = BooleanField(default=False)
        shipping_info_0 = StringField(validators=[Optional(),
                                                  Regexp(general),
                                                  Length(1, 200),
                                                  ])
        shipping_info_2 = StringField(validators=[Optional(),
                                                  Length(1, 200),
                                                  Regexp(general),
                                                  ])

        shipping_info_3 = StringField(validators=[Optional(),
                                                  Length(1, 200),
                                                  Regexp(general),
                                                  ])
        shipping_price_2 = DecimalField(validators=[Optional()])
        shipping_price_3 = DecimalField(validators=[Optional()])

        category_edit = QuerySelectField(
            query_factory=lambda: Category_Categories.query.order_by(
                Category_Categories.name.asc()).all(),
            default=lambda: Category_Categories.query.filter_by(
                cat_id=item.category_id_0).first(),
            get_label='name',

            validators=[DataRequired(message='Category is required')]
        )

        currency1 = QuerySelectField(query_factory=lambda: Query_Currency.query.all(),
                                     default=lambda: Query_Currency.query.filter_by(
            code=item.currency).first(),
            get_label='symbol',
            validators=[DataRequired(message='Currency is required')])

        item_condition_edit = QuerySelectField(query_factory=lambda: Query_ItemCondition.query.all(),
                                               default=lambda: Query_ItemCondition.query.filter(
            Query_ItemCondition.value == item.item_condition).first(),
            get_label='text',
            validators=[DataRequired(message='Item condition is required')])

        item_count_edit = QuerySelectField(query_factory=lambda: Query_ItemCount.query.all(),
                                           get_label='text',
                                           default=lambda: Query_ItemCount.query.filter_by(
            value=item.item_count).first(),
            validators=[DataRequired(message='An item count is required')])

        origin_country_1 = QuerySelectField(query_factory=lambda: Query_Country.query.all(),
                                            get_label='name',
                                            default=lambda: Query_Country.query.filter_by(
            numericcode=item.origin_country).first(),
            validators=[DataRequired(message='Origin Query_Country is Required')])

        destination11 = QuerySelectField(query_factory=lambda: Query_Country.query.all(),
                                         get_label='name',
                                         default=lambda: Query_Country.query.filter_by(
            numericcode=item.destination_country_one).first(),
            validators=[DataRequired(message='A destination Query_Country is required')])

        destination21 = QuerySelectField(query_factory=lambda: Query_Country.query.all(),
                                         get_label='name',
                                         default=lambda: Query_Country.query.filter_by(
            numericcode=item.destination_country_two).first(),
            validators=[Optional()])

        destination31 = QuerySelectField(query_factory=lambda: Query_Country.query.all(),
                                         get_label='name',
                                         default=lambda: Query_Country.query.filter_by(
            numericcode=item.destination_country_three).first(),
            validators=[Optional()])

        destination41 = QuerySelectField(query_factory=lambda: Query_Country.query.all(),
                                         get_label='name',
                                         default=lambda: Query_Country.query.filter_by(
            numericcode=item.destination_country_four).first(),
            validators=[Optional()])

        destination51 = QuerySelectField(query_factory=lambda: Query_Country.query.all(),
                                         get_label='name',
                                         default=lambda: Query_Country.query.filter_by(
            numericcode=item.destination_country_five).first(),
            validators=[Optional()])

        not_shipping_11 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                           default=lambda: Query_Continents.query.filter_by(
            value=item.not_shipping_1).first(),
            get_label='text',
            validators=[Optional()])

        not_shipping_21 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                           default=lambda: Query_Continents.query.filter_by(
            value=item.not_shipping_2).first(),
            get_label='text',
            validators=[Optional()])

        not_shipping_31 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                           default=lambda: Query_Continents.query.filter_by(
            value=item.not_shipping_3).first(),
            get_label='text',
            validators=[Optional()])

        not_shipping_41 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                           default=lambda: Query_Continents.query.filter_by(
            value=item.not_shipping_4).first(),
            get_label='text',
            validators=[Optional()])

        not_shipping_51 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                           default=lambda: Query_Continents.query.filter_by(
            value=item.not_shipping_5).first(),
            get_label='text',
            validators=[Optional()])

        notshipping61 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                         default=lambda: Query_Continents.query.filter_by(
            value=item.not_shipping_6).first(),
            get_label='text',
            validators=[Optional()])

        shipping_day_least_01 = QuerySelectField(query_factory=lambda: Query_CountLow.query.all(),
                                                 default=lambda: Query_CountLow.query.filter_by(
            value=item.shipping_day_least_0).first(),
            get_label='text',
            validators=[Optional()])

        shipping_day_most01 = QuerySelectField(query_factory=lambda: Query_CountLow.query.all(),
                                               default=lambda: Query_CountLow.query.filter_by(
            value=item.shipping_day_most_0).first(),
            get_label='text',
            validators=[Optional()])

        shipping_day_least_21 = QuerySelectField(query_factory=lambda: Query_CountLow.query.all(),
                                                 default=lambda: Query_CountLow.query.filter_by(
            value=item.shipping_day_least_2).first(),
            get_label='text',
            validators=[Optional()])

        shipping_day_most_21 = QuerySelectField(query_factory=lambda: Query_CountLow.query.all(),
                                                default=lambda: Query_CountLow.query.filter_by(
            value=item.shipping_day_most_2).first(),
            get_label='text',
            validators=[Optional()])

        shipping_day_least_31 = QuerySelectField(query_factory=lambda: Query_CountLow.query.all(),
                                                 default=lambda: Query_CountLow.query.filter_by(
            value=item.shipping_day_least_3).first(),
            get_label='text',
            validators=[Optional()])

        shipping_day_most_31 = QuerySelectField(query_factory=lambda: Query_CountLow.query.all(),
                                                default=lambda: Query_CountLow.query.filter_by(
            value=item.shipping_day_most_3).first(),
            get_label='text',
            validators=[Optional()])

        submit = SubmitField()

        def __init__(self, *args, **kwargs):
            FlaskForm.__init__(self, *args, **kwargs)

        def validate(self, *args, **kwargs):
            try:
                rv = FlaskForm.validate(self)
            except Exception as e:
                rv = False

            # verify price
            if self.price.data:
                if Decimal(self.price.data <= 0.00001):
                    return False
                else:
                    pass

                if self.shipping_two.data:
                    if self.shipping_two.data is True or self.shipping_two.data is False:
                        pass
                    else:
                        return False

                if self.shipping_three.data:
                    if self.shipping_three.data is True or self.shipping_three.data is False:
                        pass
                    else:
                        return False

            if rv:
                return True
            else:
                return False

    return vendorcreateItem


class UploadEbayForm(FlaskForm):
    ebaydata = FileField('CSV File', validators=[
        FileAllowed(['csv'],
                    DataRequired()
                    )
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
