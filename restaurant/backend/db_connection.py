from pymongo import MongoClient
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    
    # Debug: Print where we are connecting (hiding credentials)
    cluster_info = mongo_uri.split("@")[-1].split("/")[0] if "@" in mongo_uri else "localhost"
    print(f"--- DB ATTEMPT: {cluster_info} ---")
    
    # Using a very short timeout for quick response in case of failure
    # Also allowing insecure TLS to bypass local environment handshake issues
    client = MongoClient(
        mongo_uri, 
        serverSelectionTimeoutMS=3000,
        connectTimeoutMS=3000,
        tlsAllowInvalidCertificates=True
    )
    db = client["restaurant_db"] 
    return db

def check_connection():
    try:
        db = get_db()
        db.command('ping')
        return True
    except Exception:
        return False
