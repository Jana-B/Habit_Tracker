from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import bcrypt
import os
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["habittracker"]

# Function to generate hashed password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# Insert test user 'user1'
def insert_test_user():
    users_collection = db["users"]
    existing_user = users_collection.find_one({"username": "user1"})
    if existing_user:
        print("Test user already exists.")
        return "user1"
    hashed_password = hash_password("password1")
    user = {
        "username": "user1",
        "password": hashed_password
    }
    users_collection.insert_one(user)
    print(f"Inserted test user 'user1'")
    return "user1"

# Insert test habits for user1
def insert_test_habits(username):
    habits_collection = db["habits"]
    existing_habits = habits_collection.find_one({"user": username})
    
    if existing_habits:
        print("Test habits already exist for user1.")
        return
    
    # Define 3 habits
    habits = [
        {
            "user": username,
            "name": "Drinking Water",
            "color": "#00f9ff",
            "created_at": datetime.now(),
            "entries": []
        },
        {
            "user": username,
            "name": "Coffee",
            "color": "#ffae00",
            "created_at": datetime.now(),
            "entries": []
        },
        {
            "user": username,
            "name": "Daily Reading",
            "color": "#ff007f",
            "created_at": datetime.now(),
            "entries": []
        }
    ]
    
    # Insert habits into the collection
    for habit in habits:
        habits_collection.insert_one(habit)
    print("Inserted 3 test habits for user1.")

# Add 2 months of test data for habits
def add_habit_entries(username):
    habits_collection = db["habits"]
    habits = list(habits_collection.find({"user": username}))
    
    if not habits:
        print("No habits found to add entries to.")
        return
    
    start_date = datetime.now() - timedelta(days=60)  # 2 months ago

    for habit in habits:
        entries = []
        for day in range(60):
            date = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
            value = generate_random_value(habit["name"])
            entries.append({"date": date, "value": value})
        
        # Update habit with entries
        habits_collection.update_one({"_id": habit["_id"]}, {"$set": {"entries": entries}})
        print(f"Added 2 months of entries for habit: {habit['name']}")

# Generate random value based on habit
def generate_random_value(habit_name):
    if habit_name == "Drinking Water":
        return random.randint(5, 10)  # Random between 5 and 10 glasses of water
    elif habit_name == "Coffee":
        return random.randint(1, 4)  # Random between 1 and 4 cups of coffee
    elif habit_name == "Daily Reading":
        return random.choice([0, 1])  # Either 0 or 1 (read or not)
    return 0

if __name__ == "__main__":
    # Step 1: Insert test user 'user1'
    username = insert_test_user()

    # Step 2: Insert 3 test habits for 'user1'
    insert_test_habits(username)

    # Step 3: Add 2 months of daily habit tracking data
    add_habit_entries(username)

    print("Test data added successfully.")