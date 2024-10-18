# dashboard.py
import streamlit as st
from database import get_habits_collection

def show_dashboard(user_data):
    st.header("Dashboard")
    # Fetch user-specific habit data
    habits = get_habits_collection().find({"user_id": user_data['_id']})

    total_habits = habits.count()
    st.write(f"Total habits you're tracking: {total_habits}")

    # Example display of a habit
    for habit in habits:
        st.write(f"Habit: {habit['name']}, Color: {habit['color']}")

    # You can add more complex visualizations here (e.g., charts or stats)