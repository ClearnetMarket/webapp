from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from app.classes.models import QueryAdType


def add_promo_form_factory(item):
    class VendorCreatePromo(FlaskForm):
        if item == 0:
            promotype = QuerySelectField(query_factory=lambda: QueryAdType.query.all(),
                                         get_label='text',
                                         validators=[DataRequired(message='Type is Required')])



        else:
            promotype = QuerySelectField(query_factory=lambda: QueryAdType.query.all(),
                                         default=lambda: QueryAdType.query.filter_by().first(),
                                         get_label='text',
                                         validators=[DataRequired(message='Type is Required')])


        submit = SubmitField()

        def __init__(self, *args, **kwargs):
            FlaskForm.__init__(self, *args, **kwargs)

        def validate(self, *args, **kwargs):

            rv = FlaskForm.validate(self)
            if rv:
                return True
            else:
                return False

    return VendorCreatePromo


class PromoHomeForm(FlaskForm):
    submitcheckbox = SubmitField()
