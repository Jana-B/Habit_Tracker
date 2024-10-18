import streamlit as st
from models import Habit
from database import db

def habit_tab(user_id):
    habit = Habit(db, user_id)

    # Get and display user habits
    st.subheader("Your Habits")
    habits = habit.get_user_habits()

    for h in habits:
        st.write(f"**{h['name']}** (count: {h['count']})")
        col1, col2, col3 = st.columns([1, 1, 2])
        if col1.button(f"➕ Increase {h['name']}", key=h['_id']):
            habit.update_habit(h['_id'], h['count'] + 1)
            st.session_state.habits = habit.get_user_habits()  # Update session state
            st.rerun()  # Trigger rerun to reflect changes
        if col2.button(f"➖ Decrease {h['name']}", key=f"dec-{h['_id']}"):
            habit.update_habit(h['_id'], h['count'] - 1 if h['count'] > 0 else 0)
            st.session_state.habits = habit.get_user_habits()
            st.rerun()

    # Add a new habit
    st.subheader("Add New Habit")
    habit_name = st.text_input("Habit Name")
    habit_color = st.color_picker("Choose a Color", "#000000")
    if st.button("Add Habit"):
        habit.add_habit(habit_name, habit_color)
        st.session_state.habits = habit.get_user_habits()  # Refresh habits in session state
        st.rerun()

    # Handle deletion
    st.subheader("Delete Habit")
    habit_to_delete = st.selectbox("Select a habit to delete", [h['name'] for h in habits])
    if st.button("Delete"):
        habit_id = next(h['_id'] for h in habits if h['name'] == habit_to_delete)
        habit.delete_habit(habit_id)
        st.session_state.habits = habit.get_user_habits()  # Refresh habits in session state
        st.rerun()