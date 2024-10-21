import os
import certifi
from pymongo import MongoClient, ASCENDING
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

def create_unique_username_index():
    users_collection = get_user_collection()
    
    # Create a unique index on the username field
    users_collection.create_index([("username", ASCENDING)], unique=True)
    
    # print("Unique index created on username field")

# Call this function when your application starts
create_unique_username_index()