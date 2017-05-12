import mongoengine
from eve import Eve
from eve_mongoengine import EveMongoengine


class Port(mongoengine.Document):
    name = mongoengine.StringField(unique=True)


class Ship(mongoengine.Document):
    name = mongoengine.StringField(unique=True)
    type = mongoengine.StringField()


class Container(mongoengine.Document):
    product_description = mongoengine.StringField()
    discharge_rules = mongoengine.StringField()


class Consignee(mongoengine.Document):
    name = mongoengine.StringField(unique=True)


class Flight(mongoengine.Document):
    number = mongoengine.IntField()
    ship = mongoengine.ReferenceField(Ship)
    port_departure = mongoengine.ReferenceField(Port)
    port_arrival = mongoengine.ReferenceField(Port)
    departure_date = mongoengine.DateTimeField()
    arrival_date = mongoengine.DateTimeField()


class Invoice(mongoengine.Document):
    container = mongoengine.ReferenceField(Container)
    flight = mongoengine.ReferenceField(Flight)
    consignee = mongoengine.ReferenceField(Consignee)


# default eve settings
my_settings = {
    'DOMAIN': {},
    'MONGO_HOST': 'localhost',
    'MONGO_PORT': 27017,
    'MONGO_DBNAME': 'app-transportation'
}

# init application
app = Eve(settings=my_settings)
# init extension
ext = EveMongoengine(app)
# register model to eve
ext.add_model(Port)
ext.add_model(Ship)
ext.add_model(Container)
ext.add_model(Consignee)
ext.add_model(Flight)
ext.add_model(Invoice)

# let's roll
app.run(port=2323)
