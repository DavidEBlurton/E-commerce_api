from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_marshmallow import Marshmallow
from datetime import date
from typing import List
from marshmallow import ValidationError, fields
from sqlalchemy import select, delete

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Blessedone1!@localhost/ecom'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class =Base)
ma = Marshmallow(app)

class Customer(Base):
    __tablename__ = 'customer'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(db.String(75), nullable = False)
    email: Mapped[str] = mapped_column(db.String(150), nullable = True)
    phone: Mapped[str] = mapped_column(db.String(16), nullable = True)
    username: Mapped[str] = mapped_column(db.String(50), nullable = False)
    password: Mapped[str] = mapped_column(db.String(20), nullable = False)

    orders: Mapped[list["Orders"]] = db.relationship(back_populates = "customer")


order_products = db.Table(
    "orders_products",
    Base.metadata,
    db.Column('order_id', db.ForeignKey('orders.id'), primary_key = True),
    db.Column('product_id', db.ForeignKey('products.id'), primary_key = True)
)
class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key= True)
    product_name: Mapped[str] = mapped_column(db.String(500), nullable = False)
    price: Mapped[float] = mapped_column(db.Float, nullable= False)
    availability: Mapped[bool] = mapped_column(db.Boolean, default = True, nullable = False)

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key = True)
    order_date: Mapped[date] = mapped_column(db.Date, nullable = False)
    status: Mapped[str] = mapped_column(db.String(100), default = "Placed", nullable = True) 
    delivery_date: Mapped[date] = mapped_column(db.Date, nullable = True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customer.id'))

    customer: Mapped['Customer'] = db.relationship(back_populates = 'orders')

    products: Mapped[List['Products']] = db.relationship(secondary = order_products)


with app.app_context():
    ### db.drop_all()
    db.create_all()


class CustomerSchema(ma.Schema):
    id = fields.Integer(required = False)
    customer_name = fields.String(required = True)
    email = fields.String()
    phone = fields.String()
    username = fields.String(required = True)
    password = fields.String(required = True)


    class Meta:
        fields = ('id', 'customer_name', 'email', 'phone', 'username', 'password')


class ProductSchema(ma.Schema):
    id = fields.Integer(required = False)
    product_name = fields.String(required = True)
    price = fields.Float(required = True)
    availability = fields.Bool(required = True) #

    class Meta:
        fields = ('id', 'product_name', 'price', 'availability') 


class OrderSchema(ma.Schema):
    id = fields.Integer(required = False)
    order_date = fields.Date(required = False)
    customer_id = fields.Integer(required = True)
    status = fields.String(required = False)
    delivery_date = fields.Date(required = False)

    class Meta:
        fields = ('id', 'order_date', 'customer_id', 'status', 'delivery_date', 'items')


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many= True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many= True)

product_schema = ProductSchema()
products_schema = ProductSchema(many= True)


@app.route('/')
def home():
    return " Welcome to the E-Commerce application."


@app.route("/customers", methods = ['GET'])
def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars()
    customers = result.all()

    return customers_schema.jsonify(customers)


@app.route("/customers/<int:id>", methods = ['GET'])
def get_customer(id):
    query = select(Customer) .where (Customer.id == id)
    result = db.session.execute(query).scalars().first()
    
    if result is None:
        return jsonify({"Error": "Customer cannot be found"})
    
    return customer_schema.jsonify(result)


@ app.route("/customers", methods = ['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.message), 400
    
    new_customer = Customer(customer_name = customer_data['customer_name'], email= customer_data['email'], phone = customer_data['phone'], username = customer_data['username'], password = customer_data['password'])

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({'Message':"New customer information has been added."}), 201



@app.route("/customers/<int:id>", methods = ["PUT"])
def update_customer(id):
    query = select(Customer).where(Customer.id == id)
    result = db.session.execute(query).scalar()
    if result is None:
        return jsonify({"Error": "Customer cannot be found"}), 404
    
    customer = result

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        setattr(customer, field, value)

    db.session.commit()
    return jsonify({"Message":"Customer info has been updated."})

@app.route("/customers/<int:id>", methods = ["DELETE"])
def delete_customer(id):
    query = delete(Customer).where(Customer.id == id)

    result = db.session.execute(query)

    if result.rowcount == 0:
        return jsonify({"Message": "Customer cannot be found"}), 404
    
    db.session.commit()
    return jsonify({"Message": "Customer has been deleted from our database!"})


@app.route("/products", methods=['GET'])
def get_products():
    query = select(Products)
    result = db.session.execute(query).scalars()

    products = result.all()

    return products_schema.jsonify(products)


@app.route("/products/<int:id>", methods=['GET'])
def get_product(id):
    query = select(Products) .where (Products.id == id)
    result = db.session.execute(query).scalars().first()

    if result is None:
        return jsonify({"Error": "Product cannot be found"})

    return product_schema.jsonify(result)


@ app.route("/products", methods = ['POST'])
def add_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Products(product_name = product_data['product_name'], price= product_data['price'], availability= product_data['availability'])

    db.session.add(new_product)
    db.session.commit()

    return jsonify({'Message':"New product information has been added."}), 201


@app.route("/products/<int:id>", methods = ['Put'])
def update_product(id):
    query = select(Products).where(Products.id == id)
    result = db.session.execute(query).scalar()

    if result is None:
        return jsonify({"Error": "Product cannot be found"}), 404

    products = result

    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in product_data.items(): 
        setattr(products, field, value)

    db.session.commit()
    return jsonify({"Message": "Product has been updated"}) 


@app.route("/products/<int:id>", methods= ['DELETE'])
def delete_product(id):
    query = delete(Products).where(Products.id == id)

    result = db.session.execute(query)

    if result.rowcount == 0:
        return jsonify({"Message": "Product cannot be found"}), 404
    
    db.session.commit()
    return jsonify({"Message": "This Product you have selected has been deleted!"}), 200


@app.route("/orders", methods = ['POST'])
def add_order():
    try: 
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_order = Orders(order_date = date.today(), customer_id = order_data['customer_id'])

    for item_id in order_data['items']:
        query = select(Products).where(Products.id == item_id)
        item = db.session.execute(query).scalar()
        new_order.products.append(item)

    db.session.add(new_order)
    db.session.commit()
    return jsonify({"Message": "Order Placed. A date for shipping will ge given"}), 201


@app.route("/orders/<int:id>", methods=['GET'])
def get_order(id):
    query = select(Orders) .where (Orders.id == id)
    result = db.session.execute(query).scalars().first()

    if result is None:
        return jsonify({"Error": "order cannot be found"})

    return order_schema.jsonify(result)


@app.route("/orders/<int:id>", methods= ['PUT'])
def update_order_status(id):
    query = select(Orders).where(Orders.id == id)
    result = db.session.execute(query).scalar()
    if result is None:
        return jsonify({"Error": "order cannot be found"}), 404
    
    order = result
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in order_data.items():
        setattr(order, field, value)

    db.session.commit()
    return jsonify({"Message": "Order has been updated!"})   

if __name__ == "__main__":
    app.run(debug = True)