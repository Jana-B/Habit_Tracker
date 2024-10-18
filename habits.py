# habits.py
import streamlit as st
from database import get_habits_collection
from models import Habit
from bson.objectid import ObjectId  # To work with ObjectId for MongoDB

def manage_habits(user_data):
    st.header("Your Habits")

    habits = get_habits_collection().find({"user_id": ObjectId(user_data['_id'])})  # Convert user_id to ObjectId

    # Display habits with increment and decrement buttons
    for habit in habits:
        count = habit.get('count', 0)  # Use `.get('count', 0)` to provide a default value of 0 if 'count' is missing

        # Display habit name
        st.write(f"Habit: {habit['name']}")

        # Create a div for the buttons
        col1, col2, col3 = st.columns([0.02, 0.02, 0.2]) 

        with col1:
            if st.button("−", key=f"decrement-{habit['_id']}"):
                new_count = max(count - 1, 0)  # Ensure count doesn't go below 0
                Habit.update_count(habit['_id'], new_count)
                st.success(f"Decreased count for {habit['name']} to {new_count}")
                st.rerun()  # Reload to update UI

        with col2:
            st.write(f"Count: {count}", key=f"count-{habit['_id']}", classes="count-label")  # Display current count in the middle column

        with col3:
            if st.button("increase", key=f"increment-{habit['_id']}"):
                new_count = count + 1
                Habit.update_count(habit['_id'], new_count)
                st.success(f"Increased count for {habit['name']} to {new_count}")
                st.rerun()  # Reload to update UI

    # Add new habit
    st.subheader("Add a New Habit")
    habit_name = st.text_input("Habit Name")
    habit_color = st.color_picker("Choose a color", "#00f900")
    if st.button("Add Habit"):
        new_habit = Habit(user_data['_id'], habit_name, color=habit_color, count=0)  # Initialize count to 0
        new_habit.save()
        st.success(f"Habit {habit_name} added successfully!")
        st.rerun()  # Reload to show new habit