
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from models import SupplyChainManagement, Product, Supplier
from ai import SupplyChainChatbot, demand_forecast
import json
import functools

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management

scm = SupplyChainManagement()
chatbot = SupplyChainChatbot()

# Initialize with some sample data
def init_sample_data():
    supplier1 = Supplier(1, "Supplier A", "contactA@example.com")
    supplier2 = Supplier(2, "Supplier B", "contactB@example.com")

    scm.add_supplier(supplier1)
    scm.add_supplier(supplier2)

    product1 = Product(101, "Product 1", 10.0)
    product2 = Product(102, "Product 2", 20.0)
    scm.add_product_to_inventory(product1, 100)
    scm.add_product_to_inventory(product2, 50)

init_sample_data()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple hardcoded check for demonstration
        if username == 'admin' and password == 'password':
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    forecast = demand_forecast(scm)
    return render_template('index.html', scm=scm, forecast=forecast)

@app.route('/add_supplier', methods=['POST'])
@login_required
def add_supplier():
    supplier_id = int(request.form['supplier_id'])
    name = request.form['name']
    contact_info = request.form['contact_info']
    supplier = Supplier(supplier_id, name, contact_info)
    scm.add_supplier(supplier)
    return redirect(url_for('index'))

@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    product_id = int(request.form['product_id'])
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    product = Product(product_id, name, price)
    scm.add_product_to_inventory(product, quantity)
    return redirect(url_for('index'))

@app.route('/update_quantity', methods=['POST'])
@login_required
def update_quantity():
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    scm.update_product_quantity(product_id, quantity)
    return redirect(url_for('index'))

@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    order_id = int(request.form['order_id'])
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    supplier_id = int(request.form['supplier_id'])
    try:
        scm.place_order(order_id, product_id, quantity, supplier_id)
    except ValueError as e:
        return f"Error placing order: {e}", 400
    return redirect(url_for('index'))

@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot_route():
    if request.method == 'POST':
        message = request.form.get('message', '')
        response = chatbot.respond(message)
        return jsonify({'response': response})
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
