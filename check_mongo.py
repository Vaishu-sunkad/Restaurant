from restaurant.backend.db_connection import get_db

import json
import os

def check_orders():
    # 1. Check MongoDB
    try:
        db = get_db()
        orders = db["orders"]
        count = orders.count_documents({})
        print(f"📦 MongoDB Orders: {count}")
        for order in orders.find().sort("created_at", -1).limit(3):
            print(f"ID: {order['_id']} | Email: {order.get('user_email')} | Method: {order.get('payment_method')}")
    except Exception as e:
        print(f"❌ MongoDB Check Failed: {e}")

    print("-" * 30)

    # 2. Check Local Fallback
    fallback_file = "orders_fallback.json"
    if os.path.exists(fallback_file):
        try:
            with open(fallback_file, "r") as f:
                lines = f.readlines()
                print(f"💾 Local Fallback Orders: {len(lines)}")
                for line in lines[-3:]: # Show last 3
                    data = json.loads(line)
                    print(f"TIME: {data.get('created_at')} | Email: {data.get('user_email')} | Method: {data.get('payment_method')}")
                    print(f"   Details: {data.get('payment_details')}")
        except Exception as e:
            print(f"❌ Local File Read Failed: {e}")
    else:
        print("💾 No local fallback file found yet.")

if __name__ == "__main__":
    check_orders()
