from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client['habit_tracker']

# User Model
class User:
    def __init__(self, name, password, profile_image=None):
        self.name = name
        self.password = password
        self.profile_image = profile_image

    def save(self):
        return db.users.insert_one(self.__dict__)

    @staticmethod
    def find_by_name(name):
        return db.users.find_one({"name": name})

# Habit Model
class Habit:
    def __init__(self, user_id, name, color):
        self.user_id = user_id
        self.name = name
        self.color = color
        self.counter = 0
        self.history = []

    def save(self):
        return db.habits.insert_one(self.__dict__)

    @staticmethod
    def find_by_user(user_id):
        return db.habits.find({"user_id": user_id})