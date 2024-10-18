from database import get_users_collection, get_habits_collection, get_entries_collection
from models import User, Habit, Entry
from datetime import datetime

def add_sample_users():
    users_collection = get_users_collection()

    # Sample users
    sample_users = [
        {"username": "alice", "hashed_password": User.hash_password("password1")},
        {"username": "bob", "hashed_password": User.hash_password("password2")}
    ]

    for user in sample_users:
        if users_collection.find_one({"username": user["username"]}) is None:
            users_collection.insert_one(user)
            print(f"Added user: {user['username']}")
        else:
            print(f"User {user['username']} already exists")

def add_sample_habits():
    habits_collection = get_habits_collection()

    # Get user 'alice'
    user = User.find_by_username("alice")
    if not user:
        print("User 'alice' not found")
        return

    # Sample habits
    sample_habits = [
        {"user_id": user['_id'], "name": "Morning Jog", "color": "blue", "icon": "🏃‍♂️"},
        {"user_id": user['_id'], "name": "Read Book", "color": "green", "icon": "📚"}
    ]

    for habit in sample_habits:
        if habits_collection.find_one({"name": habit["name"], "user_id": user['_id']}) is None:
            habits_collection.insert_one(habit)
            print(f"Added habit: {habit['name']}")
        else:
            print(f"Habit {habit['name']} already exists")

def add_sample_entries():
    entries_collection = get_entries_collection()

    # Get habit 'Morning Jog'
    habit = get_habits_collection().find_one({"name": "Morning Jog"})
    if not habit:
        print("Habit 'Morning Jog' not found")
        return

    # Sample entries
    sample_entries = [
        {"habit_id": habit['_id'], "date": datetime(2024, 10, 1), "value": 1},
        {"habit_id": habit['_id'], "date": datetime(2024, 10, 2), "value": 1},
        {"habit_id": habit['_id'], "date": datetime(2024, 10, 3), "value": 0},
    ]

    for entry in sample_entries:
        if entries_collection.find_one({"habit_id": entry["habit_id"], "date": entry["date"]}) is None:
            entries_collection.insert_one(entry)
            print(f"Added entry for {entry['date']}")
        else:
            print(f"Entry for {entry['date']} already exists")

if __name__ == "__main__":
    add_sample_users()
    add_sample_habits()
    add_sample_entries()