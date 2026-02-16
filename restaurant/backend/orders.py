from datetime import datetime
import json
import os
from db_connection import get_db

def get_orders_collection():
    db = get_db()
    return db["orders"]

def create_order(order_data: dict):
    """
    Saves an order to the database with a local JSON fallback.
    """
    print(f"DEBUG: Incoming Order Data -> {order_data}")
    
    order_doc = {
        "customer_name": order_data.get("name"),
        "customer_mobile": order_data.get("mobile"),
        "delivery_address": order_data.get("address"),
        "special_notes": order_data.get("notes"),
        "cart": order_data.get("cart"),
        "total_amount": order_data.get("total"),
        "people_count": order_data.get("people"),
        "appetite_level": order_data.get("appetite"),
        "food_preference": order_data.get("preference"),
        "payment_method": order_data.get("payment_method"),
        "payment_details": order_data.get("payment_details"),
        "upi_id": order_data.get("upi_id"),
        "upi_app": order_data.get("upi_app"),
        "order_status": "Placed",
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
