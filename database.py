import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection string from environment variable
mongodb_uri = os.getenv('MONGODB_URI')

# MongoDB connection
client = MongoClient(mongodb_uri)
db = client['habit_tracker']

# Collections
users = db['users']
habits = db['habits']
entries = db['entries']

class User:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

    def save(self):
        return users.insert_one({
            'username': self.username,
            'hashed_password': self.hashed_password
        })

    @staticmethod
    def find_by_username(username):
        return users.find_one({'username': username})

    @staticmethod
    def find_by_id(user_id):
        return users.find_one({'_id': ObjectId(user_id)})

class Habit:
    def __init__(self, user_id, name, color=None, icon=None):
        self.user_id = user_id
        self.name = name
        self.color = color
        self.icon = icon

    def save(self):
        return habits.insert_one({
            'user_id': self.user_id,
            'name': self.name,
            'color': self.color,
            'icon': self.icon
        })

    @staticmethod
    def find_by_user(user_id):
        return list(habits.find({'user_id': user_id}))

    @staticmethod
    def find_by_id(habit_id):
        return habits.find_one({'_id': ObjectId(habit_id)})

class Entry:
    def __init__(self, habit_id, date, value):
        self.habit_id = habit_id
        self.date = date
        self.value = value

    def save(self):
        return entries.insert_one({
            'habit_id': self.habit_id,
            'date': self.date,
            'value': self.value
        })

    @staticmethod
    def find_by_habit(habit_id):
        return list(entries.find({'habit_id': habit_id}))

    @staticmethod
    def find_by_habit_and_date_range(habit_id, start_date, end_date):
        return list(entries.find({
            'habit_id': habit_id,
            'date': {'$gte': start_date, '$lte': end_date}
        }))

def init_db():
    # Create indexes
    users.create_index('username', unique=True)
    habits.create_index([('user_id', 1), ('name', 1)], unique=True)
    entries.create_index([('habit_id', 1), ('date', 1)], unique=True)

# Initialize the database
init_db()