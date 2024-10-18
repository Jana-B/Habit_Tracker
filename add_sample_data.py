from pymongo import MongoClient
from datetime import datetime, timedelta
from bcrypt import hashpw, gensalt
import random
from dotenv import load_dotenv
import os
from database import db  # Import the database instance
from models import User, Habit  # Import User and Habit classes

# Load environment variables from .env file
load_dotenv()

# Retrieve the MongoDB URI from the environment
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client['habit_tracker']

# Password hashing function
def hash_password(password):
    return hashpw(password.encode('utf-8'), gensalt())

# Sample data for two users
def create_test_data():
    user_model = User(db)  # Create an instance of User class
    user_ids = []

    # Create users and add to database
    users = [
        {"username": "user1", "hashed_password": hash_password("password1")},
        {"username": "user2", "hashed_password": hash_password("password2")},
    ]

    for user in users:
        result = user_model.create_user(user['username'], user['hashed_password'])
        user_ids.append(result.inserted_id)

    # Habit data (over a month of history for each habit)
    habit_names_user1 = ["Reading", "Meditation", "Running", "Water Intake"]
    habit_names_user2 = ["Taichi", "Coffee", "Energy Drinks", "Chocolate"]

    colors = ["#FF5733", "#33FF57", "#3357FF", "#F033FF"]
    random_counts = lambda: random.randint(0, 10)

    # Create habits for each user
    for i, user_id in enumerate(user_ids):
        habit_model = Habit(db, user_id)  # Create an instance of Habit class

        if i == 0:
            habit_names = habit_names_user1
        else:
            habit_names = habit_names_user2

        for j, name in enumerate(habit_names):
            history = []
            for day in range(1, 35):  # 34 days of history
                date = datetime.now() - timedelta(days=day)
                count = random_counts()
                history.append({"date": date, "count": count})

            # Add the habit using the Habit class
            habit_model.add_habit(name, colors[j % len(colors)])

            # Manually update the history and last_reset
            habit_model.collection.update_one(
                {"user_id": user_id, "name": name},
                {
                    "$set": {
                        "count": history[0]["count"],  # today's count
                        "last_reset": datetime.now() - timedelta(days=1)  # reset 1 day ago
                    },
                    "$set": {"history": history}  # Set the complete history
                }
            )

if __name__ == '__main__':
    create_test_data()
    print("Test data inserted successfully!")