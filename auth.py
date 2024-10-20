import bcrypt
import streamlit as st
from db import get_user_collection

# User Registration
def register_user(username, password):
    users = get_user_collection()
    if users.find_one({"username": username}):
        return False, "Username already exists"
    
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = {"username": username, "password": hashed_pw}
    users.insert_one(new_user)
    return True, "User registered successfully"

# User Login
def login_user(username, password):
    users = get_user_collection()
    user = users.find_one({"username": username})
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        return True, "Login successful"
    
    return False, "Invalid credentials"

# User Logout
def logout_user():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.success("Logged out successfully")