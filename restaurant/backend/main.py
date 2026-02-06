from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from . import auth, orders
import uvicorn

app = FastAPI()

class MobileSignup(BaseModel):
    mobile: str

class EmailSignup(BaseModel):
    email: str
    password: str

class MobileLogin(BaseModel):
    mobile: str

class EmailLogin(BaseModel):
    email: str
    password: str

class OrderItem(BaseModel):
    name: str
    price: float
    quantity: int

from typing import Optional, Any

class Order(BaseModel):
    mobile: Optional[str] = None
    email: Optional[str] = None
    cart: dict
    total: float
    people: Optional[int] = 4
    appetite: Optional[str] = None
    preference: Optional[str] = None
    payment_method: str
    payment_details: Optional[dict] = None

from .db_connection import check_connection

@app.get("/")
def read_root():
    if check_connection():
        return {"status": "backend is running", "database": "connected to Atlas"}
    return {"status": "backend is running", "database": "disconnected/local fallback"}

@app.post("/signup/mobile")
def signup_mobile(data: MobileSignup):
    if auth.create_user_mobile(data.mobile):
        return {"message": "User created"}
    raise HTTPException(status_code=400, detail="User already exists")

@app.post("/signup/email")
def signup_email(data: EmailSignup):
    if auth.create_user_email(data.email, data.password):
        return {"message": "User created"}
    raise HTTPException(status_code=400, detail="User already exists")

@app.get("/verify/mobile/{mobile}")
def verify_mobile(mobile: str):
    return {"exists": auth.verify_user_mobile(mobile)}

@app.post("/login/email")
def login_email(data: EmailLogin):
    if auth.verify_user_email(data.email, data.password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/order/place")
def place_order(data: Order):
    print(f"--- INCOMING ORDER REQUEST ---")
    print(f"Data: {data.dict()}")
    try:
        order_id = orders.create_order(data.dict())
        if order_id:
            print(f"Order Success. ID: {order_id}")
            return {"message": "Order placed successfully", "order_id": order_id}
        else:
            print("Order Failed: orders.create_order returned None")
    except Exception as e:
        print(f"Order Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=500, detail="Failed to place order")

if __name__ == "__main__":
    print("backend is starting")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
