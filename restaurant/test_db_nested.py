from backend.db_connection import get_db
import sys
import os

# Add the current directory to path so backend package is found
sys.path.append(os.getcwd())

try:
    print("Attempting to connect to MongoDB from nested backend...")
    db = get_db()
    # command to ping the database
    db.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
    print(f"Database Name: {db.name}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
