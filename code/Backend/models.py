# backend/models.py

from flask_pymongo import PyMongo

mongo = PyMongo()

def create_user(username, password, preferred_stock):
    user = {
        "username": username,
        "password": password,  # Make sure to hash passwords in production
    }
    mongo.db.users.insert_one(user)
    return user

def find_user(username):
    return mongo.db.users.find_one({"username": username})
