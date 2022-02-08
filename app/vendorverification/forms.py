from flask_wtf import FlaskForm


from wtforms import SubmitField


class vendorVerify(FlaskForm):
    levelzero = SubmitField()
    levelone = SubmitField()
    leveltwo = SubmitField()
    levelthree = SubmitField()
    levelfour = SubmitField()
    levelfive = SubmitField()
    cancel = SubmitField()


class ConfirmCancel(FlaskForm):
    confirmcancel = SubmitField()
