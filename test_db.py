from backend.db_connection import get_db
import sys
import os

# Add root to sys.path to ensure backend import works if run from inside backend or root
sys.path.append(os.getcwd())

try:
    print("Attempting to connect to MongoDB...")
    db = get_db()
    # command to ping the database
    db.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
    print(f"Database Name: {db.name}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
