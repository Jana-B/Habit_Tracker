import streamlit as st
from db import get_user_collection
from bson.objectid import ObjectId

def show_habits(user):
    st.header("Your Habits")
    user_collection = get_user_collection()
    
    habits = user['habits']
    
    # Display current habits
    for habit in habits:
        st.subheader(f"{habit['name']} ({habit['color']})")
        st.write(f"Today's progress: {habit['count']}")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"Increase {habit['name']}", key=habit['_id']):
                user_collection.update_one(
                    {"_id": user['_id'], "habits._id": ObjectId(habit['_id'])},
                    {"$inc": {"habits.$.count": 1}}
                )
                st.rerun()
        with col2:
            if st.button(f"Decrease {habit['name']}", key=f"dec_{habit['_id']}"):
                user_collection.update_one(
                    {"_id": user['_id'], "habits._id": ObjectId(habit['_id'])},
                    {"$inc": {"habits.$.count": -1}}
                )
                st.rerun()

    # Add new habit
    st.subheader("Add a New Habit")
    new_habit_name = st.text_input("Habit Name")
    new_habit_color = st.color_picker("Habit Color", "#000000")
    
    if st.button("Add Habit"):
        new_habit = {
            "_id": ObjectId(),
            "name": new_habit_name,
            "color": new_habit_color,
            "count": 0
        }
        user_collection.update_one(
            {"_id": user['_id']},
            {"$push": {"habits": new_habit}}
        )
        st.success("Habit added!")
        st.rerun()
    
    # Option to remove habits
    st.subheader("Remove a Habit")
    habit_to_remove = st.selectbox("Select habit to remove", [h['name'] for h in habits])
    
    if st.button("Remove Habit"):
        user_collection.update_one(
            {"_id": user['_id']},
            {"$pull": {"habits": {"name": habit_to_remove}}}
        )
        st.success(f"{habit_to_remove} removed!")
        st.rerun()