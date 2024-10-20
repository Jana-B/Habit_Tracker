from datetime import datetime
from db import get_habit_collection

def create_habit(name, color, userId):
    habits = get_habit_collection()
    new_habit = {
        "userId": userId,
        "name": name,
        "color": color,
        "created_at": datetime.now(),
        "entries": []  # Stores habit progress per date
    }
    habits.insert_one(new_habit)

def get_user_habits(userId):
    habits = get_habit_collection()
    return list(habits.find({"userId": userId}))

def update_habit_name(habitId, new_name):
    habits = get_habit_collection()
    habits.update_one({"_id": habitId}, {"$set": {"name": new_name}})

def delete_habit(habitId):
    habits = get_habit_collection()
    habits.delete_one({"_id": habitId})

def increment_habit(habitId, date):
    """Increases the habit count for a specific date by 1."""
    habits = get_habit_collection()
    habits.update_one(
        {"_id": habitId, "entries.date": date},
        {"$inc": {"entries.$.value": 1}}  # Increment value by 1
    )

def decrement_habit(habitId, date):
    """Decreases the habit count for a specific date by 1."""
    habits = get_habit_collection()
    habits.update_one(
        {"_id": habitId, "entries.date": date},
        {"$inc": {"entries.$.value": -1}}  # Decrement value by 1
    )

def add_entry_if_missing(habitId, date):
    """Ensures that there's an entry for the habit for the given date."""
    habits = get_habit_collection()
    habits.update_one(
        {"_id": habitId, "entries.date": {"$ne": date}},
        {"$push": {"entries": {"date": date, "value": 0}}}  # Add entry if not present
    )