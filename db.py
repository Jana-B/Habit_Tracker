import pymongo
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_db():
    client = pymongo.MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())
    return client["habittracker"]

def get_user_collection():
    db = initialize_db()
    return db['users']