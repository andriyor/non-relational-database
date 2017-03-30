from datetime import datetime
from mongoengine import *

connect('transportation')


class Ship(EmbeddedDocument):
    name = StringField(max_length=50)
    type = StringField(max_length=50)


class Flight(EmbeddedDocument):
    ship = EmbeddedDocumentField(Ship)
    port_departure = StringField(max_length=50)
    port_arrival = StringField(max_length=50)
    departure_date = DateTimeField()
    arrival_date = DateTimeField()


class Container(EmbeddedDocument):
    product_description = StringField(max_length=120)
    discharge_rules = StringField(max_length=120)


class Invoice(Document):
    container = EmbeddedDocumentField(Container)
    flight = EmbeddedDocumentField(Flight)
    consignee = StringField(max_length=120)


ship = Ship("Прилуки", "Контейнеровоз")

container = Container("Какао", "правило 1")

flight = Flight(ship, 'Ялтинський', 'Севастопольский', datetime(2017, 3, 10, 10, 45))

invoice = Invoice(container, flight, 'consignee')
invoice.save()
