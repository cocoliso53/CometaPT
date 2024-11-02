import pytest
from backend.db.data import store
from backend.db import db

@pytest.fixture
def reset_store():
    """Reset store to initial state before each test"""
    store["stock"]["beers"] = [
        {"name": "Corona", "price": 115, "quantity": 2},
        {"name": "Quilmes", "price": 120, "quantity": 0},
        {"name": "Club Colombia", "price": 110, "quantity": 3}
    ]
    store["orders"] = []
    db.order_counter = 0
    yield

def test_get_stock(reset_store):
    """Test getting the complete stock"""
    stock = db.get_stock()
    assert len(stock["beers"]) == 3
    assert stock["beers"][0]["name"] == "Corona"
    assert stock["beers"][0]["price"] == 115

def test_get_beer(reset_store):
    # Test existing beer
    beer = db.get_beer_by_name_in_stock("Corona")
    assert beer is not None
    assert beer["name"] == "Corona"
    assert beer["price"] == 115
    
    # Test non-existing beer
    beer = db.get_beer_by_name_in_stock("NonExisting")
    assert beer is None

def test_update_beer_quantity(reset_store):
    # Test successful update
    success = db.update_beer_quantity_in_stock("Corona", 5)
    assert success is True
    beer = db.get_beer_by_name_in_stock("Corona")
    assert beer["quantity"] == 5

    # Test can add more beers
    success = db.increase_beer_quantity_in_stock("Corona", 2)
    assert success is True
    beer = db.get_beer_by_name_in_stock("Corona")
    assert beer["quantity"] == 7

    # Test can't take more beers than the number in current stock
    success = db.decrease_beer_quantity_in_stock("Corona", 8)
    assert success is False    
    
    # Test updating non-existing beer
    success = db.update_beer_quantity_in_stock("NonExisting", 5)
    assert success is False

def test_create_order(reset_store):
    order_id = db.create_order()
    assert order_id == 1 
    
    order = db.get_order_by_id(order_id)
    assert order is not None
    assert order["paid"] is False
    assert order["subtotal"] == 0
    assert len(order["rounds"]) == 0

def test_add_round_to_order(reset_store):
    # Create order first
    order_id = db.create_order()
    
    # Add round
    items = [{"name": "Corona", "quantity": 2, "price":115}]
    success = db.add_round_to_order(order_id, items)
    assert success is True
    
    # Verify round was added
    order = db.get_order_by_id(order_id)
    assert len(order["rounds"]) == 1
    assert order["rounds"][0]["items"] == items

def test_get_non_existing_order(reset_store):
    order = db.get_order_by_id(999)
    assert order is None