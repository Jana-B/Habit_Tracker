import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection string from environment variable
mongodb_uri = os.getenv('MONGODB_URI')

# MongoDB connection with SSL certificate verification
client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
db = client['habit_tracker']

# Function to drop all collections in the specified database
def delete_all_data():
    # Get the list of collections
    collections = db.list_collection_names()
    
    if collections:
        for collection in collections:
            db.drop_collection(collection)
            print(f"Collection '{collection}' dropped.")
        print(f"All collections in the database '{db}' have been deleted.")
    else:
        print(f"No collections found in the database '{db}'.")

# Run the function to delete all data
if __name__ == "__main__":
    delete_all_data()

# Close the MongoDB connection
client.close()
