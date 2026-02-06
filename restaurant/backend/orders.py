from datetime import datetime
from .db_connection import get_db

def get_orders_collection():
    db = get_db()
    return db["orders"]

import json
import os

def create_order(order_data: dict):
    """
    Saves an order to the database with a local JSON fallback.
    """
    print(f"DEBUG: Incoming Order Data -> {order_data}")
    
    order_doc = {
        "user_mobile": order_data.get("mobile"),
        "user_email": order_data.get("email"),
        "cart": order_data.get("cart"),
        "total": order_data.get("total"),
        "people": order_data.get("people"),
        "appetite": order_data.get("appetite"),
        "preference": order_data.get("preference"),
        "payment_method": order_data.get("payment_method"),
        "payment_details": order_data.get("payment_details"),
        "status": "Placed",
        "created_at": datetime.utcnow().isoformat()
    }

    try:
        orders = get_orders_collection()
        result = orders.insert_one(order_doc)
        print(f"✅ Saved to MongoDB Atlas. ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        print(f"⚠️ MongoDB Failed: {str(e)}. Falling back to local file.")
        # Fallback: Save to local JSON
        try:
            with open("orders_fallback.json", "a") as f:
                f.write(json.dumps(order_doc) + "\n")
            print("💾 Saved to local orders_fallback.json")
            return "local_fallback_id"
        except Exception as fe:
            print(f"❌ Critical Failure: Could not save locally. {str(fe)}")
            return None
