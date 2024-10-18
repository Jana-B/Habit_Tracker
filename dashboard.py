# dashboard.py
import streamlit as st
from database import get_habits_collection
from bson.objectid import ObjectId

def show_dashboard(user_data):
    st.header("Dashboard")
    
    # Get the user's habits from the database
    habits_collection = get_habits_collection()

    # Use count_documents to get the total number of habits
    total_habits = habits_collection.count_documents({"user_id": ObjectId(user_data['_id'])})

    st.write(f"Total habits you're tracking: {total_habits}")

    # Fetch the actual habits to display them
    habits = habits_collection.find({"user_id": ObjectId(user_data['_id'])})

    # Display habits
    for habit in habits:
        st.write(f"Habit: {habit['name']}, Color: {habit['color']}")

    # You can add more visualizations here like charts, streaks, etc.