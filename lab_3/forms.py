from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PortForm(FlaskForm):
    port_name = StringField('Назва порту', validators=[DataRequired()])
    submit = SubmitField()


class ShipForm(FlaskForm):
    name = StringField('Імя', validators=[DataRequired()])
    type = StringField('Тип')
    submit = SubmitField()


class ContainerForm(FlaskForm):
    product_description = StringField('Опис товару', validators=[DataRequired()])
    discharge_rules = StringField('Правила розвантаження', validators=[DataRequired()])
    submit = SubmitField()


class ConsigneeForm(FlaskForm):
    consignee_name = StringField('Вантажоодержувач', validators=[DataRequired()])
    submit = SubmitField()
