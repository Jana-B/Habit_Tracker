from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta

class User:
    def __init__(self, db):
        self.collection = db['users']

    def create_user(self, username, hashed_password):
        user_data = {
            "username": username,
            "hashed_password": hashed_password,
            "profile_pic": None
        }
        return self.collection.insert_one(user_data)

    def find_user_by_username(self, username):
        return self.collection.find_one({"username": username})

    def find_user_by_id(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def update_profile_pic(self, user_id, pic_url):
        self.collection.update_one(
            {"_id": ObjectId(user_id)}, 
            {"$set": {"profile_pic": pic_url}}
        )


class Habit:
    def __init__(self, db, user_id):
        self.collection = db['habits']
        self.user_id = user_id

    def add_habit(self, name, color):
        habit_data = {
            "user_id": ObjectId(self.user_id),
            "name": name,
            "color": color,
            "count": 0,
            "history": [],
            "last_reset": datetime.now()
        }
        return self.collection.insert_one(habit_data)

    def get_user_habits(self):
        return list(self.collection.find({"user_id": ObjectId(self.user_id)}))

    def update_habit(self, habit_id, count):
        habit = self.collection.find_one({"_id": ObjectId(habit_id)})

        # Check if the day has changed and reset the counter
        if habit and habit.get("last_reset"):
            last_reset = habit["last_reset"]
            if (datetime.now() - last_reset).days >= 1:
                # Save the current count to history before resetting
                habit["history"].append({"date": last_reset, "count": habit["count"]})
                count = 1  # Reset the count for the new day

        # Update the habit count and the reset date
        self.collection.update_one(
            {"_id": ObjectId(habit_id)},
            {
                "$set": {"count": count, "last_reset": datetime.now()},
                "$push": {"history": {"date": datetime.now(), "count": count}}
            }
        )

    def reset_habit(self, habit_id):
        self.collection.update_one(
            {"_id": ObjectId(habit_id)},
            {
                "$set": {"count": 0},
                "$push": {"history": {"date": datetime.now(), "count": 0}}
            }
        )

    def delete_habit(self, habit_id):
        self.collection.delete_one({"_id": ObjectId(habit_id)})