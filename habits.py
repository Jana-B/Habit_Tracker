# habits.py
import streamlit as st
from database import get_habits_collection
from models import Habit

def manage_habits(user_data):
    st.header("Your Habits")
    
    habits = get_habits_collection().find({"user_id": user_data['_id']})

    # Display habits
    for habit in habits:
        st.write(f"Habit: {habit['name']}")
        if st.button(f"Delete {habit['name']}", key=f"delete-{habit['_id']}"):
            get_habits_collection().delete_one({"_id": habit['_id']})
            st.success(f"Habit {habit['name']} deleted")
            st.rerun()

    # Add new habit
    st.subheader("Add a New Habit")
    habit_name = st.text_input("Habit Name")
    habit_color = st.color_picker("Choose a color", "#00f900")
    if st.button("Add Habit"):
        new_habit = Habit(user_data['_id'], habit_name, color=habit_color)
        new_habit.save()
        st.success(f"Habit {habit_name} added successfully!")
        st.rerun()