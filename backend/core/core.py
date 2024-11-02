from datetime import datetime
from functools import reduce
from backend.db import db

# constant to keep track of tax rate, better placed ina different layer?? 
TAX_RATE = 0.16

def add_price_to_item(item):
    beer = db.get_beer_by_name_in_stock(item["name"])
    price = beer["price"]
    updated_item = item | {"price": price}
    return updated_item

def calculate_total_per_item(item):
    price = item["price"]
    quantity = item["quantity"]
    total = price * quantity
    return total

def calculate_round_total(items):
    items_with_price = list(map(add_price_to_item,items))
    total_per_item = list(map(calculate_total_per_item,items_with_price))
    round_total = sum(total_per_item)
    return round_total


def create_new_order():
    order_id = db.create_order()
    return db.get_order_by_id(order_id)

def add_round(order_id, items):
    order = db.get_order_by_id(order_id)
    if not order:
        return False, "Order not found"
    
    if order["paid"]:
        return False, "Cannot modify a paid order"

    # Check we have enough beers
    for item in items:
        beer = db.get_beer_by_name_in_stock(item["name"])
        if not beer:
            return False, f"We dont sell {item['name']}"
        if beer["quantity"] < item["quantity"]:
            return False, f"Not enough {item['name']} beers to fulfill order"

    # Update db, here we iterate because we only care about the side effects
    for item in items:
        beer = db.get_beer_by_name_in_stock(item["name"])
        db.decrease_beer_quantity_in_stock(beer["name"],item["quantity"])

    # Add round to order and update totals
    if db.add_round_to_order(order_id, items):
        order = db.get_order_by_id(order_id)
        round_total = calculate_round_total(items)
        order["subtotal"] += round_total
        order["taxes"] += round_total*TAX_RATE
        return True, "Round added successfully"
    
    return False, "Failed to add round"

def apply_discount(order_id, discount_amount):
    order = db.get_order_by_id(order_id)
    if not order:
        return False, "Order not found"
    
    if order["paid"]:
        return False, "Cannot modify a paid order"
    
    if discount_amount > order["subtotal"]: #could also check discount amount to be greater than 0
        return False, "Discount cannot be greater than subtotal"

    order["discounts"] = discount_amount
    return True, "Discount applied successfully"

def get_order_total(order_id):
    order = db.get_order_by_id(order_id)
    if not order:
        return False, "Order not found", 0
    
    total = order["subtotal"] + order["taxes"] - order["discounts"]

    return total

def pay_order(order_id):
    order = db.get_order_by_id(order_id)
    if order["paid"]:
        return False, "Order is already paid", 0
    
    total = get_order_total(order_id)
    
    if db.update_order_paid(order_id):
        return True, "Order paid successfully", total
    
    return False, "Failed to update order status", 0


### TBD if we keep this one
def get_order_details(order_id):
    """
    Get detailed order information including all calculations
    """
    order = db.get_order_by_id(order_id)
    if not order:
        return None
    
    # Create a summary of beers ordered
    beer_summary = {}
    for round in order["rounds"]:
        for item in round["items"]:
            beer = db.get_beer_by_name_in_stock(item["name"])
            if beer:
                if item["name"] not in beer_summary:
                    beer_summary[item["name"]] = {
                        "quantity": 0,
                        "price_per_unit": beer["price"],
                        "total": 0
                    }
                beer_summary[item["name"]]["quantity"] += item["quantity"]
                beer_summary[item["name"]]["total"] += beer["price"] * item["quantity"]

    return {
        "id": order["id"],
        "created": order["created"],
        "paid": order["paid"],
        "rounds": order["rounds"],
        "beer_summary": beer_summary,
        "subtotal": order["subtotal"],
        "taxes": order["taxes"],
        "discounts": order["discounts"],
        "total": order["subtotal"] + order["taxes"] - order["discounts"]
    }