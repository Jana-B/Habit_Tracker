import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Connection
ca = certifi.where()
client = MongoClient(os.getenv("MONGO_URI"), tlsCAFile=ca)
db = client['habittracker']

def get_user_collection():
    return db['users']

def get_habit_collection():
    return db['habits']