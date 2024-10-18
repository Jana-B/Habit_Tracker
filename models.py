from database import get_users_collection, get_habits_collection, get_entries_collection
import bcrypt
from bson.objectid import ObjectId

class User:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

    def save(self):
        return get_users_collection().insert_one({
            'username': self.username,
            'hashed_password': self.hashed_password
        })

    @staticmethod
    def find_by_id(user_id):
        return get_users_collection().find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def find_by_username(username):
        return get_users_collection().find_one({'username': username})

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def verify_password(plain_password, hashed_password):
        # Check if hashed_password is already in bytes
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')  # Convert to bytes if it's a string
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

class Habit:
    def __init__(self, user_id, name, color=None, icon=None):
        self.user_id = user_id
        self.name = name
        self.color = color
        self.icon = icon

    def save(self):
        return get_habits_collection().insert_one({
            'user_id': self.user_id,
            'name': self.name,
            'color': self.color,
            'icon': self.icon
        })
        
    @staticmethod
    def find_by_user_id(user_id):
        return list(get_habits_collection().find({'user_id': user_id}))

class Entry:
    def __init__(self, habit_id, date, value):
        self.habit_id = habit_id
        self.date = date
        self.value = value

    def save(self):
        return get_entries_collection().insert_one({
            'habit_id': self.habit_id,
            'date': self.date,
            'value': self.value
        })