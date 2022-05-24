from app import app, db
from flask import url_for, redirect, render_template, request
import plivo
from app.models import Order


def send_sms_notification(to, message_body, callback_url):
    client = plivo.RestClient(app.config['PLIVO_AUTH_ID'],app.config['PLIVO_AUTH_TOKEN'])
    response = client.messages.create(
            src=app.config['PLIVO_NUMBER'],
            dst=to, 
            text=message_body, 
            url=callback_url)
    print(response)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add/', methods=['POST', 'GET'])
def add():
    return render_template('user.html')


@app.route('/add/orders', methods=['POST'])
def add_orders():
    customer_name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    order = Order(customer_name=customer_name,
                  customer_phone_number=phone_number)
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('order_index'))


@app.route('/orders')
def order_index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)


@app.route('/order/<order_id>')
def order_show(order_id):
    order = Order.query.get(order_id)

    return render_template('show.html', order=order)


@app.route('/order/<order_id>/pickup', methods=['POST'])
def order_pickup(order_id):
    order = Order.query.get(order_id)
    order.status = 'Shipped'
    order.notification_status = 'queued'
    db.session.commit()

    callback_url = request.base_url.replace('/pickup', '') + '/notification/status/update'
    send_sms_notification(order.customer_phone_number,
                          'Your food is ready and on its way to you!',
                          callback_url)

    return redirect(url_for('order_show', order_id=order_id))


@app.route('/order/<order_id>/deliver', methods=['POST'])
def order_deliver(order_id):
    order = Order.query.get(order_id)
    order.status = 'Delivered'
    order.notification_status = 'queued'
    db.session.commit()

    callback_url = request.base_url.replace('/deliver', '') + '/notification/status/update'
    send_sms_notification(order.customer_phone_number,
                          'Your food is arriving now.', callback_url)

    return redirect(url_for('order_index'))


@app.route('/order/<order_id>/notification/status/update',
           methods=['POST'])
def order_deliver_status(order_id):
    order = Order.query.get(order_id)
    order.notification_status = request.form['Status']
    db.session.commit()

    return render_template('show.html', order=order)