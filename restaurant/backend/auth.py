from datetime import datetime
import random
from db_connection import get_db

def get_collection():
    db = get_db()
    return db["users"]

def create_user_mobile(mobile):
    """
    Creates a new user with mobile number. 
    Returns True if created, False if already exists.
    """
    users = get_collection()
    if users.find_one({"mobile": mobile}):
        return False
    
    user = {
        "mobile": mobile,
        "created_at": datetime.utcnow(),
        "type": "mobile"
    }
    users.insert_one(user)
    return True

def create_user_email(email, password):
    """
    Creates a new user with email and password.
    Returns True if created, False if already exists.
    """
    users = get_collection()
    if users.find_one({"email": email}):
        return False
    
    user = {
        "email": email,
        "password": password, # In production, hash this!
        "created_at": datetime.utcnow(),
        "type": "email"
    }
    users.insert_one(user)
    return True

def verify_user_mobile(mobile):
    """
    Checks if a mobile user exists.
    """
    users = get_collection()
    user = users.find_one({"mobile": mobile})
    return user is not None

def verify_user_email(email, password):
    """
    Verifies email and password.
    """
    users = get_collection()
    user = users.find_one({"email": email, "password": password})
    return user is not None
