from flask import Flask, request, jsonify, json, render_template
from flask_sqlalchemy import SQLAlchemy
from utils import *

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:?charset=utf-8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.Integer)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    order = db.relationship("Order")
    user = db.relationship("User")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


# Создаем БД
db.create_all()

users = fill_users_data(User, get_data_json("data/user_data.json"))
db.session.add_all(users)
db.session.commit()

orders = fill_orders_data(Order, get_data_json("data/order_data.json"))
db.session.add_all(orders)
db.session.commit()

offers = fill_offer_data(Offer, get_data_json("data/offer_data.json"))
db.session.add_all(offers)
db.session.commit()


@app.route("/users", methods=["GET", "POST"])
def get_users(user_data=None):
    if request.method == "GET":
        result = []
        users = User.query.all()
        for user in users:
            result.append(user.to_dict())
        return jsonify(result)

    if request.method == "POST":
        user_data = json.loads(request.data)

        new_user_data = new_user(User, user_data)
        db.session.add(new_user_data)
        db.session.commit()

        return "Пользователь добавлен", 201


@app.route("/users/<int:id_user>", methods=["GET", "PUT", "DELETE"])
def get_one_user(id_user):
    if request.method == "GET":
        user = User.query.get(id_user)
        return jsonify(user.to_dict())

    if request.method == "PUT":
        user_data = json.loads(request.data)
        user = User.query.get(id_user)

        user.id = user_data["id"]
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.age = user_data["age"]
        user.email = user_data["email"]
        user.role = user_data["role"]
        user.phone = user_data["phone"]

        db.session.add(user)
        db.session.commit()

        return "Пользователь обновлен", 201

    if request.method == "DELETE":
        user = User.query.get(id_user)

        db.session.delete(user)
        db.session.commit()

        return "Пользователь удален", 201


@app.route("/orders", methods=["GET", "POST"])
def get_orders():
    if request.method == "GET":

        result = []
        orders = Order.query.all()
        for order in orders:
            result.append(order.to_dict())

        return jsonify(result)

    if request.method == "POST":
        order_data = json.loads(request.data)

        new_order_data = new_order(Order, order_data)
        db.session.add(new_order_data)
        db.session.commit()

        return "Новый заказ добавлен", 201


@app.route("/orders/<int:id_orders>", methods=["GET", "PUT", "DELETE"])
def get_one_order(id_orders):
    if request.method == "GET":
        order = Order.query.get(id_orders)
        return jsonify(order.to_dict())

    if request.method == "PUT":
        order_data = json.loads(request.data)
        order = Order.query.get(id_orders)

        order.id = order_data["id"]
        order.name = order_data["name"]
        order.description = order_data["description"]
        order.start_date = order_data["start_date"]
        order.end_date = order_data["end_date"]
        order.address = order_data["address"]
        order.price = order_data["price"]
        order.customer_id = order_data["customer_id"]
        order.executor_id = order_data["executor_id"]

        db.session.add(order)
        db.session.commit()

        return "Заказ обновлен", 201

    if request.method == "DELETE":
        order = Order.query.get(id_orders)

        db.session.delete(order)
        db.session.commit()

        return "Заказ удален", 201


@app.route("/offers", methods=["GET", "POST"])
def get_offers():
    if request.method == "GET":

        result = []
        offers_data = Offer.query.all()
        for offer in offers_data:
            result.append(offer.to_dict())

        return jsonify(result)

    if request.method == "POST":
        offer_data = json.loads(request.data)

        new_offer_data = new_offer(Offer, offer_data)
        db.session.add(new_offer_data)
        db.session.commit()

        return "Новый заказ размещен", 201


@app.route("/offers/<int:id_offer>", methods=["GET", "PUT", "DELETE"])
def get_one_offer(id_offer):
    if request.method == "GET":
        offer = Offer.query.get(id_offer)
        return jsonify(offer.to_dict())

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        offer = Offer.query.get(id_offer)

        offer.id = offer_data["id"]
        offer.order_id = offer_data["order_id"]
        offer.executor_id = offer_data["executor_id"]

        db.session.add(offer)
        db.session.commit()

        return "Заказ обновлен", 201

    if request.method == "DELETE":
        offer = Offer.query.get(id_offer)

        db.session.delete(offer)
        db.session.commit()

        return "Заказ удален", 201


if __name__ == '__main__':
    app.run(debug=True)
