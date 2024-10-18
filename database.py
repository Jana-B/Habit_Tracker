import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection string from environment variable
mongodb_uri = os.getenv('MONGODB_URI')

# MongoDB connection with SSL certificate verification
client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
db = client['habit_tracker']

# Collections
users = db['users']
habits = db['habits']


def get_users_collection():
    return users

def get_habits_collection():
    return habits

