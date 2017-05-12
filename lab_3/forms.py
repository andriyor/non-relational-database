from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField, IntegerField
from wtforms.validators import DataRequired


class PortForm(FlaskForm):
    name = StringField('Назва порту', validators=[DataRequired()])
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
    name = StringField('Вантажоодержувач', validators=[DataRequired()])
    submit = SubmitField()


class FlightForm(FlaskForm):
    number = IntegerField('Номер Рейсу')
    ship = SelectField('Cудно', choices=[])
    port_departure = SelectField('Порт відправлення', choices=[])
    port_arrival = SelectField('Порт прибуття', choices=[])
    departure_date = DateTimeField('Departure Date', format='%d.%m.%Y %H:%M')
    arrival_date = DateTimeField('Arrival Date', format='%d.%m.%Y %H:%M')
    submit = SubmitField()


class InvoiceForm(FlaskForm):
    container = SelectField('Контейнер', choices=[])
    flight = SelectField('Номер рейсу', choices=[])
    consignee = SelectField('Вантажоодержувач', choices=[])
    submit = SubmitField()


class FindShipForm(FlaskForm):
    container_product_description = StringField()
    submit = SubmitField()
