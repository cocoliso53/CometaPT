from datetime import datetime
from .data import store, order_counter

def get_stock():
    """Get's all current stock"""
    return store["stock"]

def get_beer_by_name_in_stock(name):
    matches = list(filter(lambda beer: beer["name"] == name, store["stock"]["beers"]))
    return matches[0] if matches else None

def update_beer_quantity_in_stock(name, quantity):
    beer = get_beer_by_name_in_stock(name)
    if beer and (quantity >= 0): # move to business logic layer
        beer["quantity"] = quantity
        store["stock"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return True
    return False


## these two functions could be generalized
def increase_beer_quantity_in_stock(name, amount):
    beer = get_beer_by_name_in_stock(name)
    if beer and (amount > 0): # move to business logic layer
        current_quantity = beer["quantity"]
        new_quantity = current_quantity + amount
        return update_beer_quantity_in_stock(name,new_quantity)
    return False

def decrease_beer_quantity_in_stock(name,amount):
    beer = get_beer_by_name_in_stock(name)
    if beer and (amount > 0): # move to business logic layer
        current_quantity = beer["quantity"]
        new_quantity = current_quantity - amount
        return update_beer_quantity_in_stock(name, new_quantity)
    return False

def create_order():
    global order_counter
    order_counter += 1
    
    new_order = {
        "id": order_counter,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "paid": False,
        "subtotal": 0,
        "taxes": 0,
        "discounts": 0,
        "items": [],
        "rounds": []
    }
    
    store["orders"].append(new_order)
    return order_counter

def get_order_by_id(order_id):
    matches = list(filter(lambda order: order["id"] == order_id, store["orders"]))
    return matches[0] if matches else None

def add_round_to_order(order_id, items):
    order = get_order_by_id(order_id)
    if order:
        new_round = {
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": items
        }
        order["rounds"].append(new_round)
        return True
    return False

def update_order_paid(order_id):
    order = get_order_by_id(order_id)
    if order:
        order["paid"] = True
        return True
    return False