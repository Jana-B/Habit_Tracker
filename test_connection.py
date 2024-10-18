from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection string from environment variable
mongodb_uri = os.getenv('MONGODB_URI')

# MongoDB connection with SSL certificate verification
client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
db = client['habit_tracker']

# Test connection
def test_connection():
    try:
        # Fetch collection names
        collections = db.list_collection_names()
        print(f"Connected to the database. Collections: {collections}")
        return True
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return False

if __name__ == "__main__":
    test_connection()