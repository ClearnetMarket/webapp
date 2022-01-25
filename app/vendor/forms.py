from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from wtforms import \
    StringField, \
    SubmitField, \
    TextAreaField, \
    SelectField, \
    BooleanField, \
    FileField, \
    DecimalField

from wtforms.validators import DataRequired, Length, Regexp, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.auth.validation import general
from app.common.query import sortbyrating
from app.classes.category import Categories

from app.classes.models import \
    Currency, \
    Query_Carriers, \
    Query_Count_low, \
    Query_Continents, \
    Query_Itemcondition, \
    Query_Itemcount, \
    Country

from decimal import Decimal


class newOrders(FlaskForm):
    turnoff = BooleanField()
    submitcheckbox = SubmitField()


class acceptedOrders(FlaskForm):
    turnoff = BooleanField()
    submitcheckbox = SubmitField()


class deactive(FlaskForm):
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

    selectcarrier3 = QuerySelectField(query_factory=lambda: Query_Carriers.query.all(), get_label='text')

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


class ConfirmCancel(FlaskForm):
    confirmcancel = SubmitField()


class vendorVerify(FlaskForm):
    levelzero = SubmitField()
    levelone = SubmitField()
    leveltwo = SubmitField()
    levelthree = SubmitField()
    levelfour = SubmitField()
    levelfive = SubmitField()
    cancel = SubmitField()


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


def add_product_form_factory(item):
    class vendorcreateItem(FlaskForm):
        btc_accepted = BooleanField(default=True)
        btc_cash_accepted = BooleanField(default=True)

        itemtitlee = StringField(validators=[DataRequired(message="A title is required for your listing"),
                                             Length(1, 100),
                                             Regexp(general),
                                             ])

        itemrefundpolicy = TextAreaField(validators=[Optional(),
                                                     Regexp(general),
                                                     Length(1, 500),
                                                     ])

        pricee = DecimalField(validators=[DataRequired(message='Item Price is Required'),
                                          ])

        itemdescription = TextAreaField(validators=[
            DataRequired(message='Item Description is Required'),
            Regexp(general),
            Length(5, 1500)])

        details = BooleanField(default=False)

        details1 = StringField(validators=[Optional(),
                                           Length(1, 50),
                                           Regexp(general)])

        details1answer = StringField(validators=[Optional(),
                                                 Length(1, 50),
                                                 Regexp(general)])

        details2 = StringField(validators=[Optional(),
                                           Length(1, 50),
                                           Regexp(general)])
        details2answer = StringField(validators=[ Optional(),
                                                  Length(1, 50),
                                                  Regexp(general)])

        details3 = StringField(validators=[Optional(),
                                           Length(1, 50),
                                           Regexp(general)])

        details3answer = StringField(validators=[Optional(),
                                                 Length(1, 50),
                                                 Regexp(general)])

        details4 = StringField(validators=[Optional(),
                                           Length(1, 50),
                                           Regexp(general)])

        details4answer = StringField(validators=[Optional(),
                                                 Length(1, 50),
                                                 Regexp(general)])

        details5 = StringField(validators=[Optional(),
                                           Length(1, 50),
                                           Regexp(general)])

        details5answer = StringField(validators=[Optional(),
                                                 Length(1, 50),
                                                 Regexp(general)])

        details6 = StringField(validators=[Optional(),
                                           Length(1, 50),
                                           Regexp(general)])

        details6answer = StringField(validators=[Optional(),
                                                 Length(1, 50),
                                                 Regexp(general)])

        details7 = StringField(validators=[Optional(),
                                           Length(1, 50),
                                           Regexp(general)])

        details7answer = StringField(validators=[Optional(),
                                                 Length(1, 50),
                                                 Regexp(general)])

        details8 = StringField(validators=[Optional(),
                                           Length(1, 50),
                                           Regexp(general)])

        details8answer = StringField(validators=[Optional(),
                                                 Length(1, 50),
                                                 Regexp(general)])

        details9 = StringField(validators=[Optional(),
                                           Length(1, 50),
                                           Regexp(general)])

        details9answer = StringField(validators=[Optional(),
                                                 Length(1, 50),
                                                 Regexp(general)])

        details10 = StringField(validators=[Optional(),
                                            Length(1, 50),
                                            Regexp(general)])

        details10answer = StringField(validators=[Optional(),
                                                  Length(1, 50),
                                                  Regexp(general)])



        imageone1 = FileField('Primary Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                       message='Images only or wrong format')
                                                           ])

        imagetwo = FileField('Upload Image 2', validators=[Optional(),
                                                           FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                       message='Images only or wrong format')
                                                           ])

        imagethree = FileField('Upload Image 3', validators=[Optional(),
                                                             FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                         message='Images only or wrong format')
                                                             ])

        imagefour = FileField('Upload Image 4', validators=[Optional(),
                                                            FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                        message='Images only or wrong format')
                                                            ])

        imagefive = FileField('Upload Image 5', validators=[Optional(),
                                                            FileAllowed(['jpg', 'png', 'gif', 'png', 'jpeg'],
                                                                        message='Images only or wrong format')
                                                            ])

        keywords = StringField(validators=[
            DataRequired(message='Keywords are the terms used to find your item in the search results.  '
                                 'They are required'),
            Length(5, 200),
            Regexp(general)]
        )

        return_this_item = BooleanField(default=False)
        shippingfree = BooleanField(default=False)
        shippingtwo = BooleanField(default=False)
        shippingthree = BooleanField(default=False)
        shippinginfo0 = StringField(validators=[Optional(),
                                                Regexp(general),
                                                Length(1, 200),
                                                ])
        shippinginfo2 = StringField(validators=[Optional(),
                                                Length(1, 200),
                                                Regexp(general),
                                                ])

        shippinginfo3 = StringField(validators=[Optional(),
                                                Length(1, 200),
                                                Regexp(general),
                                                ])
        shippingprice2 = DecimalField(validators=[Optional()])
        shippingprice3 = DecimalField(validators=[Optional()])
        submit = SubmitField()

        if item == 0:
            category = QuerySelectField(query_factory=lambda: Categories.query.order_by(Categories.name.asc()).all(),
                                        get_label='name',
                                        validators=[DataRequired(message='Category is required')])

            currency = QuerySelectField(query_factory=lambda: Currency.query.all(),
                                        get_label='symbol',
                                        validators=[DataRequired(message='Currency is required')])

            itemcondition = QuerySelectField(query_factory=lambda: Query_Itemcondition.query.all(),
                                             get_label='text',
                                             validators=[DataRequired(message='Item condition is required')])

            itemcount = QuerySelectField(query_factory=lambda: Query_Itemcount.query.all(),
                                         get_label='text',
                                         validators=[DataRequired(message='An item count is required')])

            origincountry = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             validators=[DataRequired(message="Item Origin is required")])

            destination1 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                            get_label='name',
                                            validators=[DataRequired(message='One Destination is required')])

            destination2 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                            get_label='name',
                                            validators=[Optional()])

            destination3 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                            get_label='name',
                                            validators=[Optional()])

            destination4 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                            get_label='name',
                                            validators=[Optional()])

            destination5 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                            get_label='name',
                                            validators=[Optional()])

            notshipping1 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                            get_label='text',
                                            validators=[Optional()])

            notshipping2 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                            get_label='text',
                                            validators=[Optional()])

            notshipping3 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                            get_label='text',
                                            validators=[Optional()])

            notshipping4 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                            get_label='text',
                                            validators=[Optional()])

            notshipping5 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                            get_label='text',
                                            validators=[Optional()])

            notshipping6 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                            get_label='text',
                                            validators=[Optional()])

            shippingdayleast0 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                 get_label='text',
                                                 validators=[Optional()])

            shippingdaymost0 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                get_label='text',
                                                validators=[Optional()])

            shippingdayleast2 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                 get_label='text',
                                                 validators=[Optional()])

            shippingdaymost2 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                get_label='text',
                                                validators=[Optional()])

            shippingdayleast3 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                 get_label='text',
                                                 validators=[Optional()])

            shippingdaymost3 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                get_label='text',
                                                validators=[Optional()])

        else:

            category_edit = QuerySelectField(
                query_factory=lambda: Categories.query.order_by(Categories.name.asc()).all(),

                default=lambda: Categories.query.order_by(Categories.name.asc()).all(),
                get_label='name',
                validators=[DataRequired(message='Category is required')]
            )

            currency1 = QuerySelectField(query_factory=lambda: Currency.query.all(),
                                         default=lambda: Currency.query.filter_by(code=item.currency).first(),
                                         get_label='symbol',
                                         validators=[DataRequired(message='Currency is required')])

            itemcondition_edit = QuerySelectField(query_factory=lambda: Query_Itemcondition.query.all(),
                                                  default=lambda: Query_Itemcondition.query.filter(
                                                      Query_Itemcondition.value == item.itemcondition).first(),
                                                  get_label='text',
                                                  validators=[DataRequired(message='Item condition is required')])

            itemcount_edit = QuerySelectField(query_factory=lambda: Query_Itemcount.query.all(),
                                              get_label='text',
                                              default=lambda: Query_Itemcount.query.filter_by(value=item.itemcount).first(),
                                              validators=[DataRequired(message='An item count is required')])

            origincountry1 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                              get_label='name',
                                              default=lambda: Country.query.filter_by(numericcode=item.origincountry).first(),
                                              validators=[DataRequired(message='Origin Country is Required')])

            destination11 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(numericcode=item.destinationcountry).first(),
                                             validators=[DataRequired(message='A destination Country is required')])

            destination21 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(numericcode=item.destinationcountrytwo).first(),
                                             validators=[Optional()])

            destination31 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(numericcode=item.destinationcountrythree).first(),
                                             validators=[Optional()])

            destination41 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(numericcode=item.destinationcountryfour).first(),
                                             validators=[Optional()])

            destination51 = QuerySelectField(query_factory=lambda: Country.query.all(),
                                             get_label='name',
                                             default=lambda: Country.query.filter_by(numericcode=item.destinationcountryfive).first(),
                                             validators=[Optional()])

            notshipping11 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                             default=lambda: Query_Continents.query.filter_by(value=item.notshipping1).first(),
                                             get_label='text',
                                             validators=[Optional()])

            notshipping21 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                             default=lambda: Query_Continents.query.filter_by(value=item.notshipping2).first(),
                                             get_label='text',
                                             validators=[Optional()])

            notshipping31 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                             default=lambda: Query_Continents.query.filter_by(value=item.notshipping3).first(),
                                             get_label='text',
                                             validators=[Optional()])

            notshipping41 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                             default=lambda: Query_Continents.query.filter_by(value=item.notshipping4).first(),
                                             get_label='text',
                                             validators=[Optional()])

            notshipping51 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                             default=lambda: Query_Continents.query.filter_by(value=item.notshipping5).first(),
                                             get_label='text',
                                             validators=[Optional()])

            notshipping61 = QuerySelectField(query_factory=lambda: Query_Continents.query.all(),
                                             default=lambda: Query_Continents.query.filter_by(value=item.notshipping6).first(),
                                             get_label='text',
                                             validators=[Optional()])

            shippingdayleast01 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                  default=lambda: Query_Count_low.query.filter_by(value=item.shippingdayleast0).first(),
                                                  get_label='text',
                                                  validators=[Optional()])

            shippingdaymost01 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                 default=lambda: Query_Count_low.query.filter_by(value=item.shippingdaymost0).first(),
                                                 get_label='text',
                                                 validators=[Optional()])

            shippingdayleast21 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                  default=lambda: Query_Count_low.query.filter_by(value=item.shippingdayleast2).first(),
                                                  get_label='text',
                                                  validators=[Optional()])

            shippingdaymost21 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                 default=lambda: Query_Count_low.query.filter_by(value=item.shippingdaymost2).first(),
                                                 get_label='text',
                                                 validators=[Optional()])

            shippingdayleast31 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                  default=lambda: Query_Count_low.query.filter_by(value=item.shippingdayleast3).first(),
                                                  get_label='text',
                                                  validators=[Optional()])

            shippingdaymost31 = QuerySelectField(query_factory=lambda: Query_Count_low.query.all(),
                                                 default=lambda: Query_Count_low.query.filter_by(value=item.shippingdaymost3).first(),
                                                 get_label='text',
                                                 validators=[Optional()])

        def __init__(self, *args, **kwargs):
            FlaskForm.__init__(self, *args, **kwargs)

        def validate(self, *args, **kwargs):
            try:
                rv = FlaskForm.validate(self)
            except Exception as e:
                rv = False

            # verify price
            if self.pricee.data:
                if Decimal(self.pricee.data <= 0.00001):
                    return False
                else:
                    pass

                if self.shippingtwo.data:
                    if self.shippingtwo.data is True or self.shippingtwo.data is False:
                        pass
                    else:
                        return False

                if self.shippingthree.data:
                    if self.shippingthree.data is True or self.shippingthree.data is False:
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
