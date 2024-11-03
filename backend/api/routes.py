from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.core import core
from backend.db import db
from datetime import datetime

# Models
class OrderItem(BaseModel):
    name: str
    quantity: int

class RoundRequest(BaseModel):
    items: List[OrderItem]

class DiscountRequest(BaseModel):
    amount: float

class OrderSummary(BaseModel):
    id: int
    created: str
    paid: bool
    subtotal: float
    taxes: float
    discounts: float
    total: float

app = FastAPI(title="APP")

### Stock
### We could add some other functions like update stock 
### in case of aquiring beer from a provider, or some similar functionallity

@app.get("/stock")
async def get_stock():
    """Get current stock of beers"""
    return db.get_stock()

### Orders

@app.post("/orders", response_model=OrderSummary)
async def create_order():
    order = core.create_new_order()
    if not order:
        raise HTTPException(status_code=500, detail="Failed to create order")
    
    return core.get_order_details(order["id"])

@app.post("/orders/{order_id}/rounds")
async def add_round_to_order(order_id: int, round_data: RoundRequest):
    items_dict = [item.model_dump() for item in round_data.items]
    success, message = core.add_round(order_id, items_dict)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return core.get_order_details(order_id)

@app.post("/orders/{order_id}/discount")
async def apply_discount_to_order(order_id: int, discount_data: DiscountRequest):
    success, message = core.apply_discount(order_id, discount_data.amount)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return core.get_order_details(order_id)

@app.post("/orders/{order_id}/pay")
async def pay_order(order_id: int):
    success, message, total = core.pay_order(order_id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "message": message,
        "total": total,
        "order": core.get_order_details(order_id)
    }

@app.get("/orders/{order_id}")
async def get_order_details(order_id: int):
    order_details = core.get_order_details(order_id)
    
    if not order_details:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order_details

### Non exhaustive list of posible endpoints, but it covers the basics