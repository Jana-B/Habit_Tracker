import streamlit as st
from auth import login, logout, signup, get_user
from dashboard import show_dashboard
from habit import show_habits
from userprofile import show_profile
from db import initialize_db

# Initialize MongoDB connection
db = initialize_db()

# Sidebar Navigation
st.sidebar.title("Habit Tracker App")
menu = st.sidebar.radio("Go to", ["Dashboard", "Habits", "Profile", "Login", "Sign Up"])

user = get_user()  # Retrieve logged-in user

if menu == "Dashboard" and user:
    show_dashboard(user)
elif menu == "Habits" and user:
    show_habits(user)
elif menu == "Profile" and user:
    show_profile(user)
elif menu == "Login":
    login()
elif menu == "Sign Up":
    signup()
else:
    st.write("Please log in to access the app")

# Logout option
if user:
    if st.sidebar.button("Logout"):
        logout()