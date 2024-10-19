import streamlit as st
import bcrypt
from db import get_user_collection

session_key = 'logged_in_user'

def get_user():
    return st.session_state.get(session_key)

def login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user_collection = get_user_collection()
        user = user_collection.find_one({"username": username})
        
        if user and bcrypt.checkpw(password.encode(), user['password']):
            st.session_state[session_key] = user
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def signup():
    st.header("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        user_collection = get_user_collection()
        existing_user = user_collection.find_one({"username": username})
        
        if existing_user:
            st.error("Username already exists")
        else:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user_collection.insert_one({"username": username, "password": hashed_password, "habits": []})
            st.success("Account created! Please log in.")

def logout():
    st.session_state.pop(session_key, None)
    st.rerun()