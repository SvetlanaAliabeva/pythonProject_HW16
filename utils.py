import json


def get_data_json(f):
    with open(f, "r", encoding="UTF-8") as file:
        return json.load(file)


def fill_users_data(user_class, json_data):
    result = []
    for user in json_data:
        current_user = user_class(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            age=user["age"],
            email=user["email"],
            role=user["role"],
            phone=user["phone"]
        )
        result.append(current_user)

    return result


def fill_orders_data(order_class, json_data):
    result = []
    for order in json_data:
        current_order = order_class(
            id=order["id"],
            name=order["name"],
            description=order["description"],
            start_date=order["start_date"],
            end_date=order["end_date"],
            address=order["address"],
            price=order["price"],
            customer_id=order["customer_id"],
            executor_id=order["executor_id"]
        )
        result.append(current_order)

    return result


def fill_offer_data(offer_class, json_data):
    result = []
    for offer in json_data:
        current_offer = offer_class(
            id=offer["id"],
            order_id=offer["order_id"],
            executor_id=offer["executor_id"]
        )
        result.append(current_offer)

    return result


def new_user(user_class, data):
    user = user_class(
        id=data["id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        email=data["email"],
        role=data["role"],
        phone=data["phone"]
    )
    return user


def new_order(order_class, data):
    order = order_class(
        id=data["id"],
        name=data["name"],
        description=data["description"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        address=data["address"],
        price=data["price"],
        customer_id=data["customer_id"],
        executor_id=data["executor_id"]
    )
    return order


def new_offer(offer_class, data):
    offer = offer_class(
        id=data["id"],
        order_id=data["order_id"],
        executor_id=data["executor_id"]
    )
    return offer
