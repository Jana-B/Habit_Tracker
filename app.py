import streamlit as st
from database import get_habits_collection
from models import User
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from dashboard import show_dashboard
from habits import manage_habits
from userprofile import manage_profile

def main():
    st.set_page_config(layout="wide")  # For better layout with the sidebar

    st.title("Habit Tracker")

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    if st.session_state.user_id is None:
        tab1, tab2 = st.tabs(["Login", "Register"])

        # Login Tab
        with tab1:
            st.header("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user_data = User.find_by_username(username)
                if user_data and User.verify_password(password, user_data['hashed_password']):
                    st.session_state.user_id = str(user_data['_id'])  # Store as string
                    st.success(f"Logged in successfully! Hello {user_data['username']}.")
                    st.rerun()  # Reload after login
                else:
                    st.error("Invalid username or password")

        # Registration Tab
        with tab2:
            st.header("Register")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            if st.button("Register"):
                if new_username and new_password:
                    hashed_password = User.hash_password(new_password)
                    new_user = User(new_username, hashed_password)
                    try:
                        new_user.save()
                        st.success("Registration successful! Please log in.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Please enter both username and password")

    else:
        # If user is logged in
        user_data = User.find_by_id(st.session_state.user_id)

        if user_data:
            st.sidebar.title(f"Hello, {user_data['username']}!")

            # Sidebar tabs
            tab_selection = st.sidebar.radio("Navigate", ["Dashboard", "Habits", "Profile"])

            if tab_selection == "Dashboard":
                show_dashboard(user_data)
            elif tab_selection == "Habits":
                manage_habits(user_data)
            elif tab_selection == "Profile":
                manage_profile(user_data)

            if st.sidebar.button("Logout"):
                st.session_state.user_id = None
                st.rerun()  # Reload to show login screen

        else:
            st.error("User data not found. Please log in again.")
            st.session_state.user_id = None
            st.rerun()  # Reset if user data is corrupted

if __name__ == "__main__":
    main()