from flask import render_template, request, Blueprint
from .models import Port, Ship, Container, Consignee, Flight, Invoice
from .forms import PortForm, ShipForm, ContainerForm, ConsigneeForm

tr_app = Blueprint('todo_app', __name__, template_folder='templates')


@tr_app.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@tr_app.app_errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@tr_app.route("/add_port/", methods=['GET', 'POST'])
def add_port():
    form = PortForm()
    if form.validate_on_submit():
        Port(port_name=form.port_name.data).save()
    return render_template('add.html', form=form)


@tr_app.route("/add_ship/", methods=['GET', 'POST'])
def add_ship():
    form = ShipForm()
    if form.validate_on_submit():
        Ship(name=form.name.data, type=form.type.data).save()
    return render_template('add.html', form=form)


@tr_app.route("/add_container/", methods=['GET', 'POST'])
def add_container():
    form = ContainerForm()
    if form.validate_on_submit():
        Container(product_description=form.product_description.data,
                  discharge_rules=form.discharge_rules.data).save()
    return render_template('add.html', form=form)


@tr_app.route("/add_consignee/", methods=['GET', 'POST'])
def add_consignee():
    form = ConsigneeForm()
    if form.validate_on_submit():
        Consignee(consignee_name=form.consignee_name.data).save()
    return render_template('add.html', form=form)


@tr_app.route("/search_flight", methods=['GET', 'POST'])
def search_flight():
    ports = Port.objects
    if request.method == 'POST':
        port_departure_id = request.values.get("port_departure_id")
        port_departure = Port.objects.get(id=port_departure_id)

        port_arrival_id = request.values.get("port_arrival_id")
        port_arrival = Port.objects.get(id=port_arrival_id)

        departure_date = request.values.get("departure_date")
        arrival_date = request.values.get("departure_date")

    return render_template('search_flight.html', ports=ports)


@tr_app.route("/add_flight", methods=['GET', 'POST'])
def add_flight():
    ports = Port.objects
    ships = Ship.objects
    if request.method == 'POST':
        ship_id = request.values.get("ship_id")
        ship = Ship.objects.get(id=ship_id)

        port_departure_id = request.values.get("port_departure_id")
        port_departure = Port.objects.get(id=port_departure_id)

        port_arrival_id = request.values.get("port_arrival_id")
        port_arrival = Port.objects.get(id=port_arrival_id)

        departure_date = request.values.get("departure_date")
        arrival_date = request.values.get("departure_date")

        Flight(ship=ship, port_departure=port_departure, port_arrival=port_arrival,
               departure_date=departure_date, arrival_date=arrival_date).save()
    return render_template('add_flight.html', ships=ships, ports=ports)


@tr_app.route("/add_invoice", methods=['GET', 'POST'])
def add_invoice():
    containers = Container.objects
    flights = Flight.objects
    consignees = Consignee.objects
    if request.method == 'POST':
        container_id = request.values.get("container_id")
        container = Container.objects.get(id=container_id)

        flight_id = request.values.get("flight_id")
        flight = Flight.objects.get(id=flight_id)

        consignee_id = request.values.get("consignee_id")
        consignee = Consignee.objects.get(id=consignee_id)

        Invoice(container=container, flight=flight, consignee=consignee).save()
    return render_template('add_invoices.html', containers=containers,
                           flights=flights, consignees=consignees)
