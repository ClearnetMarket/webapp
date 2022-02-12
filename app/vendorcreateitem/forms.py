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

from app.classes.category import Categories

from app.classes.models import \
    Currency, \
    Query_Count_low, \
    Query_Continents, \
    Query_item_condition, \
    Query_item_count, \
    Country


def add_product_info(item):
    class CreateItemInfo(FlaskForm):
        btc_accepted = BooleanField(default=True)
        btc_cash_accepted = BooleanField(default=True)

        item_title = StringField(validators=[DataRequired(message="A title is required for your listing"),
                                             Length(1, 100),
                                             Regexp(general),
                                             ])

        price = DecimalField(validators=[DataRequired(message='Item Price is Required'),
                                         ])

        keywords = StringField(validators=[
            DataRequired(message='Keywords are the terms used to find your item in the search results.  '
                                 'They are required'),
            Length(5, 200),
            Regexp(general)]
        )

        submit = SubmitField()

        if item == 0:
            category = QuerySelectField(query_factory=lambda: Categories.query.order_by(Categories.name.asc()).all(),
                                        get_label='name',
                                        allow_blank=True,
                                        blank_text=u'-- Select Category --',
                                        validators=[DataRequired(message='Category is required')])

            currency = QuerySelectField(query_factory=lambda: Currency.query.all(),
                                        get_label='symbol',
                                        allow_blank=True,
                                        blank_text=u'-- Select Fiat Currency --',
                                        validators=[DataRequired(message='Currency is required')])

            item_condition = QuerySelectField(query_factory=lambda: Query_item_condition.query.all(),
                                              get_label='text',
                                              allow_blank=True,
                                              blank_text=u'-- Select Item Condition --',
                                              validators=[DataRequired(message='Item condition is required')])

            item_count = QuerySelectField(query_factory=lambda: Query_item_count.query.all(),
                                          get_label='text',
                                          allow_blank=False,
                                          validators=[DataRequired(message='An item count is required')])

        else:

            category_edit = QuerySelectField(
                query_factory=lambda: Categories.query.order_by(
                    Categories.name.asc()).all(),
                default=lambda: Categories.query.filter_by(
                    cat_id=item.category_id_0).first(),
                get_label='name',

                validators=[DataRequired(message='Category is required')]
            )

            currency1 = QuerySelectField(query_factory=lambda: Currency.query.all(),
                                         default=lambda: Currency.query.filter_by(
                                             code=item.currency).first(),
                                         get_label='symbol',
                                         validators=[DataRequired(message='Currency is required')])

            item_condition_edit = QuerySelectField(query_factory=lambda: Query_item_condition.query.all(),
                                                   default=lambda: Query_item_condition.query.filter(
                Query_item_condition.value == item.item_condition).first(),
                get_label='text',
                validators=[DataRequired(message='Item condition is required')])

            item_count_edit = QuerySelectField(query_factory=lambda: Query_item_count.query.all(),
                                               get_label='text',
                                               default=lambda: Query_item_count.query.filter_by(
                value=item.item_count).first(),
                validators=[DataRequired(message='An item count is required')])

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
            if rv:
                return True
            else:
                return False

    return CreateItemInfo


class CreateItemImages(FlaskForm):

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

    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):
        try:
            rv = FlaskForm.validate(self)
        except Exception as e:
            rv = False
        if rv:
            return True
        else:
            return False


class CreateInfoDescription(FlaskForm):

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
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self, *args, **kwargs):
        try:
            rv = FlaskForm.validate(self)
        except Exception as e:
            rv = False

        if rv:
            return True
        else:
            return False


def add_product_shipping(item):
    class CreateShipping(FlaskForm):

        item_refund_policy = TextAreaField(validators=[Optional(),
                                                       Regexp(general),
                                                       Length(1, 500),
                                                       ])

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
        submit = SubmitField()

        if item == 0:

            origin_country = QuerySelectField(query_factory=lambda: Country.query.order_by(Country.id.asc()).all(),
                                              get_label='name',
                                              allow_blank=True,
                                              blank_text=u'-- Select Origin Country --',
                                              validators=[DataRequired(message="Item Origin is required")])

            destination1 = QuerySelectField(query_factory=lambda: Country.query.order_by(Country.id.asc()).all(),
                                            get_label='name',
                                            allow_blank=True,
                                            blank_text=u'-- please choose --',
                                            validators=[DataRequired(message='One Destination is required')])

            destination2 = QuerySelectField(query_factory=lambda: Country.query.order_by(Country.id.asc()).all(),
                                            default=lambda: Country.query.filter_by(
                                                numericcode=0).first(),
                                            get_label='name',
                                            allow_blank=True,
                                            blank_text=u'-- Optional --',
                                            validators=[Optional()])

            destination3 = QuerySelectField(query_factory=lambda: Country.query.order_by(Country.id.asc()).all(),
                                            default=lambda: Country.query.filter_by(
                                                numericcode=0).first(),
                                            get_label='name',
                                            allow_blank=True,
                                            blank_text=u'-- Optional --',
                                            validators=[Optional()])

            destination4 = QuerySelectField(query_factory=lambda: Country.query.order_by(Country.id.asc()).all(),
                                            default=lambda: Country.query.filter_by(
                                                numericcode=0).first(),
                                            get_label='name',
                                            allow_blank=True,
                                            blank_text=u'-- Optional --',
                                            validators=[Optional()])

            destination5 = QuerySelectField(query_factory=lambda: Country.query.order_by(Country.id.asc()).all(),
                                            default=lambda: Country.query.filter_by(
                                                numericcode=0).first(),
                                            get_label='name',
                                            allow_blank=True,
                                            blank_text=u'-- Optional --',
                                            validators=[Optional()])

            not_shipping_1 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                              get_label='text',
                                              allow_blank=True,
                                              blank_text=u'-- Optional --',
                                              validators=[Optional()])

            not_shipping_2 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                              get_label='text',
                                              allow_blank=True,
                                              blank_text=u'-- Optional --',
                                              validators=[Optional()])

            not_shipping_3 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                              get_label='text',
                                              allow_blank=True,
                                              blank_text=u'-- Optional --',
                                              validators=[Optional()])

            not_shipping_4 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                              get_label='text',
                                              allow_blank=True,
                                              blank_text=u'-- Optional --',
                                              validators=[Optional()])

            not_shipping_5 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                              get_label='text',
                                              allow_blank=True,
                                              blank_text=u'-- Optional --',
                                              validators=[Optional()])

            not_shipping_6 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                              get_label='text',
                                              allow_blank=True,
                                              blank_text=u'-- Optional --',
                                              validators=[Optional()])

            shipping_day_least_0 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                    get_label='text',
                                                    allow_blank=True,
                                                    validators=[Optional()])

            shipping_day_most_0 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                   get_label='text',
                                                   allow_blank=True,

                                                   validators=[Optional()])

            shipping_day_least_2 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                    get_label='text',
                                                    allow_blank=True,
                                                    validators=[Optional()])

            shipping_day_most_2 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                   get_label='text',
                                                   allow_blank=True,
                                                   validators=[Optional()])

            shipping_day_least_3 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                    get_label='text',
                                                    validators=[Optional()])

            shipping_day_most_3 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                   get_label='text',
                                                   validators=[Optional()])

        else:

            origin_country_1 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                                get_label='name',
                                                default=lambda: Country.query.filter_by(
                numericcode=item.origin_country).first(),
                validators=[DataRequired(message='Origin Country is Required')])

            destination11 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(
                                                 numericcode=item.destination_country_one).first(),
                                             validators=[DataRequired(message='A destination Country is required')])

            destination21 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(
                                                 numericcode=item.destination_country_two).first(),
                                             validators=[Optional()])

            destination31 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(
                                                 numericcode=item.destination_country_three).first(),
                                             validators=[Optional()])

            destination41 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(
                                                 numericcode=item.destination_country_four).first(),
                                             validators=[Optional()])

            destination51 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(
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

            shipping_day_least_01 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                     default=lambda: Query_Count_low.query.filter_by(
                value=item.shipping_day_least_0).first(),
                get_label='text',
                validators=[Optional()])

            shipping_day_most01 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                   default=lambda: Query_Count_low.query.filter_by(
                value=item.shipping_day_most_0).first(),
                get_label='text',
                validators=[Optional()])

            shipping_day_least_21 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                     default=lambda: Query_Count_low.query.filter_by(
                value=item.shipping_day_least_2).first(),
                get_label='text',
                validators=[Optional()])

            shipping_day_most_21 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                    default=lambda: Query_Count_low.query.filter_by(
                value=item.shipping_day_most_2).first(),
                get_label='text',
                validators=[Optional()])

            shipping_day_least_31 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                     default=lambda: Query_Count_low.query.filter_by(
                value=item.shipping_day_least_3).first(),
                get_label='text',
                validators=[Optional()])

            shipping_day_most_31 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                    default=lambda: Query_Count_low.query.filter_by(
                value=item.shipping_day_most_3).first(),
                get_label='text',
                validators=[Optional()])

        def __init__(self, *args, **kwargs):
            FlaskForm.__init__(self, *args, **kwargs)

        def validate(self, *args, **kwargs):
            try:
                rv = FlaskForm.validate(self)
            except Exception as e:
                rv = False

            if rv:
                return True
            else:
                return False

    return CreateShipping
