from fastapi.testclient import TestClient
import pytest
from backend.db.data import store
from backend.db import db
from backend.api.routes import app

client = TestClient(app)

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

def test_get_stock(reset_store):
    response = client.get("/stock")
    assert response.status_code == 200
    assert "beers" in response.json()
    assert len(response.json()["beers"]) == 3

def test_create_order(reset_store):
    response = client.post("/orders")
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["paid"] is False

def test_add_round(reset_store):
    # Create the order first
    order_response = client.post("/orders")
    order_id = order_response.json()["id"]
    
    # Add a round to recently created order
    round_data = {
        "items": [
            {"name": "Corona", "quantity": 2}
        ]
    }
    response = client.post(f"/orders/{order_id}/rounds", json=round_data)
    
    assert response.status_code == 200
    assert response.json()["subtotal"] == 230

def test_apply_discount(reset_store):
    order_response = client.post("/orders")
    order_id = order_response.json()["id"]
    
    round_data = {
        "items": [
            {"name": "Corona", "quantity": 2}
        ]
    }
    client.post(f"/orders/{order_id}/rounds", json=round_data)
    
    # Apply the discount
    discount_data = {"amount": 50}
    response = client.post(f"/orders/{order_id}/discount", json=discount_data)
    
    assert response.status_code == 200
    assert response.json()["discounts"] == 50

def test_pay_order(reset_store):
    # Create order and add items
    order_response = client.post("/orders")
    order_id = order_response.json()["id"]
    
    round_data = {
        "items": [
            {"name": "Corona", "quantity": 2}
        ]
    }
    client.post(f"/orders/{order_id}/rounds", json=round_data)
    
    # Pay order
    response = client.post(f"/orders/{order_id}/pay")
    
    assert response.status_code == 200
    assert "total" in response.json()
    assert response.json()["order"]["paid"] is True

def test_get_order(reset_store):
    # Create order
    order_response = client.post("/orders")
    order_id = order_response.json()["id"]
    
    # Get order details
    response = client.get(f"/orders/{order_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == order_id

def test_get_non_existent_order(reset_store):
    """Test getting non-existent order"""
    response = client.get("/orders/999")
    assert response.status_code == 404