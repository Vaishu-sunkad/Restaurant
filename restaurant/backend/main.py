from typing import Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
import auth
import orders
import uvicorn
from db_connection import check_connection, get_db

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

class Order(BaseModel):
    name: str
    mobile: str
    address: str
    notes: Optional[str] = None
    cart: dict
    total: float
    people: Optional[int] = 4
    appetite: Optional[str] = None
    preference: Optional[str] = None
    payment_method: str
    payment_details: Optional[dict] = None
    upi_id: Optional[str] = None
    upi_app: Optional[str] = None


@app.get("/")
def read_root():
    status_info = get_backend_status()
    return status_info

@app.get("/health")
def health_check():
    """Simple health check"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

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

@app.get("/status")
def get_backend_status():
    """Comprehensive backend status check"""
    try:
        # Check database connection
        db_status = check_connection()
        
        # Check collections
        if db_status:
            try:
                db = get_db()
                collections = db.list_collection_names()
                orders_count = db["orders"].count_documents({})
                users_count = db["users"].count_documents({})
                
                return {
                    "status": "healthy",
                    "database": "connected",
                    "mongodb_details": {
                        "database": "restaurant_db",
                        "collections": collections,
                        "orders_count": orders_count,
                        "users_count": users_count
                    },
                    "endpoints": {
                        "order_place": "/order/place (POST)",
                        "get_orders": "/orders (GET)",
                        "get_order": "/order/{id} (GET)",
                        "auth_endpoints": "Available"
                    }
                }
            except Exception as db_e:
                return {
                    "status": "partial",
                    "database": "connection_error",
                    "error": str(db_e)
                }
        else:
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "fallback": "local_json_available"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/orders")
def get_all_orders():
    """Get all orders to verify data is stored"""
    try:
        orders_collection = orders.get_orders_collection()
        all_orders = list(orders_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id
        return {"orders": all_orders, "count": len(all_orders)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/order/{order_id}")
def get_order(order_id: str):
    """Get specific order by ID"""
    try:
        orders_collection = orders.get_orders_collection()
        order = orders_collection.find_one({"_id": ObjectId(order_id)}, {"_id": 0})
        if order:
            return order
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
def get_all_users():
    """Get all users to verify authentication system"""
    try:
        users_collection = get_db()["users"]
        all_users = list(users_collection.find({}, {"_id": 0, "password": 0}))  # Exclude sensitive data
        return {"users": all_users, "count": len(all_users)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
