import pytest
from backend.core import core
from backend.db.data import store
from backend.db import db

@pytest.fixture
def reset_store():
    """Reset store to initial state before each test"""
    store["stock"]["beers"] = [
        {"name": "Corona", "price": 115, "quantity": 10},
        {"name": "Quilmes", "price": 120, "quantity": 10},
        {"name": "Club Colombia", "price": 110, "quantity": 10}
    ]
    store["orders"] = []
    db.order_counter = 0
    yield

def test_create_new_order(reset_store):
    """Test order creation"""
    order = core.create_new_order()
    assert order is not None
    assert order["paid"] is False
    assert order["subtotal"] == 0
    assert len(order["rounds"]) == 0

def test_add_round(reset_store):
    """Test adding a round to an order"""
    # Create order
    order = core.create_new_order()
    
    # Add round
    items = [{"name": "Corona", "quantity": 2}]
    success, message = core.add_round(order["id"], items)
    
    assert success is True
    assert message == "Round added successfully"
    
    # Verify order details
    order_details = core.get_order_details(order["id"])
    assert order_details["subtotal"] == 230  # 2 * 115
    
    # Verify stock was updated
    corona = db.get_beer_by_name_in_stock("Corona")
    assert corona["quantity"] == 8  # Initial 10 - 2

def test_add_round_insufficient_stock(reset_store):
    """Test adding a round with insufficient stock"""
    order = core.create_new_order()
    items = [{"name": "Corona", "quantity": 20}]  # More than available
    
    success, message = core.add_round(order["id"], items)
    assert success is False

def test_apply_discount(reset_store):
    """Test applying discount to an order"""
    # Create and add items to order
    order = core.create_new_order()
    items = [{"name": "Corona", "quantity": 2}]
    core.add_round(order["id"], items)
    
    # Apply discount
    success, message = core.apply_discount(order["id"], 50)
    assert success is True
    
    # Verify discount
    order_details = core.get_order_details(order["id"])
    assert order_details["discounts"] == 50

def test_pay_order(reset_store):
    """Test paying an order"""
    # Create and add items to order
    order = core.create_new_order()
    items = [{"name": "Corona", "quantity": 2}]
    core.add_round(order["id"], items)
    
    # Pay order
    success, message, total = core.pay_order(order["id"])
    assert success is True
    
    # Verify order is marked as paid
    order_details = core.get_order_details(order["id"])
    assert order_details["paid"] is True

def test_get_order_details(reset_store):
    """Test getting detailed order information"""
    # Create and add items to order
    order = core.create_new_order()
    items = [{"name": "Corona", "quantity": 2}]
    core.add_round(order["id"], items)
    
    # Get details
    details = core.get_order_details(order["id"])
    
    assert details is not None
    assert "beer_summary" in details
    assert "Corona" in details["beer_summary"]
    assert details["beer_summary"]["Corona"]["quantity"] == 2
    assert details["beer_summary"]["Corona"]["total"] == 230