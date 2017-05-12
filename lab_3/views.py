from flask import render_template, request, Blueprint, redirect, url_for, flash
from .models import Port, Ship, Container, Consignee, Flight, Invoice
from lab_3.forms import PortForm, ShipForm, ContainerForm, ConsigneeForm, FlightForm, InvoiceForm, FindShipForm
from datetime import datetime

tr_app = Blueprint('tr_app', __name__, template_folder='templates')


@tr_app.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@tr_app.app_errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@tr_app.route("/add_port/", methods=['GET', 'POST'])
def add_port():
    form = PortForm()
    ports = Port.objects
    if form.validate_on_submit():
        Port(name=form.name.data).save()
    return render_template('add_port.html', form=form, ports=ports)


@tr_app.route('/update_port/<string:port_id>', methods=['GET', 'POST'])
def update_port(port_id):
    form = PortForm(request.form)
    port = Port.objects.get(id=port_id)
    if form.validate_on_submit():
        port.update(name=form.name.data)
        return redirect(url_for('tr_app.add_port'))
    return render_template('update_port.html', form=form, port=port)


@tr_app.route('/delete_port/<string:port_id>')
def delete_port(port_id):
    Port.objects.get(id=port_id).delete()
    return redirect(url_for('tr_app.add_port'))


@tr_app.route("/add_ship/", methods=['GET', 'POST'])
def add_ship():
    form = ShipForm()
    ships = Ship.objects
    if form.validate_on_submit():
        Ship(name=form.name.data, type=form.type.data).save()
    return render_template('add_ship.html', form=form, ships=ships)


# TODO fix IndexError: list index out of range
@tr_app.route('/update_ship/<string:ship_id>', methods=['GET', 'POST'])
def update_ship(ship_id):
    form = ShipForm(request.form)
    ship = Ship.objects.get(id=ship_id)
    if form.validate_on_submit():
        ship.update(name=form.name.data, type=form.type.data)
        return redirect(url_for('tr_app.add_ship'))
    return render_template('update_ship.html', form=form, ship=ship)


@tr_app.route('/delete_ship/<string:ship_id>')
def delete_ship(ship_id):
    Ship.objects.get(id=ship_id).delete()
    return redirect(url_for('tr_app.add_ship'))


@tr_app.route("/add_container/", methods=['GET', 'POST'])
def add_container():
    form = ContainerForm()
    containers = Container.objects
    if form.validate_on_submit():
        Container(product_description=form.product_description.data,
                  discharge_rules=form.discharge_rules.data).save()
    return render_template('add_container.html', form=form, containers=containers)


@tr_app.route('/update_container/<string:container_id>', methods=['GET', 'POST'])
def update_container(container_id):
    form = ContainerForm(request.form)
    container = Container.objects.get(id=container_id)
    if form.validate_on_submit():
        container.update(product_description=form.product_description.data,
                         discharge_rules=form.discharge_rules.data)
        return redirect(url_for('tr_app.add_container'))
    return render_template('update_container.html', form=form, container=container)


@tr_app.route('/delete_container/<string:container_id>')
def delete_container(container_id):
    Container.objects.get(id=container_id).delete()
    return redirect(url_for('tr_app.add_container'))


@tr_app.route("/add_consignee/", methods=['GET', 'POST'])
def add_consignee():
    form = ConsigneeForm()
    consignees = Consignee.objects
    if form.validate_on_submit():
        Consignee(name=form.name.data).save()
    return render_template('add_consignee.html', form=form, consignees=consignees)


@tr_app.route('/update_consignee/<string:consignee_id>', methods=['GET', 'POST'])
def update_consignee(consignee_id):
    form = ConsigneeForm(request.form)
    consignee = Consignee.objects.get(id=consignee_id)
    if form.validate_on_submit():
        consignee.update(name=form.name.data)
        return redirect(url_for('tr_app.add_consignee'))
    return render_template('update_consignee.html', form=form, consignee=consignee)


@tr_app.route('/delete_consignee/<string:consignee_id>')
def delete_consignee(consignee_id):
    Consignee.objects.get(id=consignee_id).delete()
    return redirect(url_for('tr_app.add_consignee'))


@tr_app.route("/add_flight", methods=['GET', 'POST'])
def add_flight():
    free_ship = Ship.objects(id__nin=[flight.ship.id for flight in Flight.objects(arrival_date__gt=datetime.now())])
    ships = ([(str(ship.id), ship.name) for ship in free_ship])
    ports = ([(str(port.id), port.name) for port in Port.objects])

    form = FlightForm()
    form.ship.choices = ships
    form.port_arrival.choices = ports
    form.port_departure.choices = ports

    flights = Flight.objects
    if form.validate_on_submit():
        if form.port_departure.data == form.port_arrival.data:
            flash('port departure and port arrival must be different')
        if form.arrival_date.data <= form.departure_date.data:
            flash('arrival date must be great then departure date')
        else:
            Flight(number=form.number.data, ship=form.ship.data, port_departure=form.port_departure.data,
                   port_arrival=form.port_arrival.data,
                   departure_date=form.departure_date.data,
                   arrival_date=form.arrival_date.data).save()
    return render_template('add_flight.html', form=form, flights=flights)


@tr_app.route('/update_flight/<string:flight_id>', methods=['GET', 'POST'])
def update_flight(flight_id):
    flight = Flight.objects.get(id=flight_id)

    ships = ([(str(ship.id), ship.name) for ship in Ship.objects])
    ports = ([(str(port.id), port.name) for port in Port.objects])

    form = FlightForm()
    form.ship.choices = ships
    form.port_arrival.choices = ports
    form.port_departure.choices = ports
    if form.validate_on_submit():
        flight.update(number=form.number.data, ship=Ship.objects.get(id=form.ship.data),
                      port_departure=Port.objects.get(id=form.port_departure.data),
                      port_arrival=Port.objects.get(id=form.port_arrival.data),
                      departure_date=form.departure_date.data,
                      arrival_date=form.arrival_date.data
                      )
        return redirect(url_for('tr_app.add_flight'))
    return render_template('update_flight.html', form=form, flight=flight)


@tr_app.route('/delete_flight/<string:flight_id>')
def delete_flight(flight_id):
    Flight.objects.get(id=flight_id).delete()
    return redirect(url_for('tr_app.add_flight'))


@tr_app.route("/add_invoice", methods=['GET', 'POST'])
def add_invoice():
    containers = ([(str(container.id), container.product_description) for container in Container.objects])
    consignees = ([(str(consignee.id), consignee.name) for consignee in Consignee.objects])
    flights = ([(str(flight.id), str(flight.number)) for indexss, flight in enumerate(Flight.objects)])

    form = InvoiceForm()
    form.container.choices = containers
    form.flight.choices = flights
    form.consignee.choices = consignees

    invoices = Invoice.objects
    if form.validate_on_submit():
        container = Container.objects.get(id=form.container.data)
        flight = Flight.objects.get(id=form.flight.data)
        consignee = Consignee.objects.get(id=form.consignee.data)
        Invoice(container=container, flight=flight, consignee=consignee).save()
    return render_template('add_invoices.html', form=form, invoices=invoices)


@tr_app.route('/add_invoice/<string:invoice_id>')
def delete_invoice(invoice_id):
    Invoice.objects.get(id=invoice_id).delete()
    return redirect(url_for('tr_app.add_invoice'))


@tr_app.route('/update_invoice/<string:invoice_id>', methods=['GET', 'POST'])
def update_invoice(invoice_id):
    containers = ([(str(container.id), container.product_description) for container in Container.objects])
    consignees = ([(str(consignee.id), consignee.name) for consignee in Consignee.objects])
    flights = ([(str(flight.id), str(flight.number)) for indexss, flight in enumerate(Flight.objects)])
    form = InvoiceForm()
    form.container.choices = containers
    form.flight.choices = flights
    form.consignee.choices = consignees

    invoice = Invoice.objects.get(id=invoice_id)
    if form.validate_on_submit():
        container = Container.objects.get(id=form.container.data)
        flight = Flight.objects.get(id=form.flight.data)
        consignee = Consignee.objects.get(id=form.consignee.data)
        invoice.update(container=container, flight=flight, consignee=consignee)
        return redirect(url_for('tr_app.add_invoice'))
    return render_template('update_invoice.html', form=form, invoice=invoice)


@tr_app.route('/find_ship', methods=['GET', 'POST'])
def find_ship():
    form = FindShipForm()
    ships = ''
    if form.validate_on_submit():
        cd = form.container_product_description.data
        conteiners = [container.id for container in Container.objects(product_description=cd)]
        ships = [invoice.flight.ship for invoice in Invoice.objects(container__in=conteiners)]
        return render_template('show_ship_by_container_desc.html', ships=ships, form=form)
    return render_template('show_ship_by_container_desc.html', ships=ships, form=form)
