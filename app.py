import streamlit as st
from models import User

def main():
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
                    st.session_state.user_id = user_data['_id']
                    st.success("Logged in successfully!")
                    st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
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
        user_data = User.find_by_username(st.session_state.user_id)
        
        # Check if user_data is None
        if user_data is not None:
            st.write(f"Welcome back, {user_data['username']}!")
        else:
            st.error("User data not found. Please log in again.")
        
        if st.button("Logout"):
            st.session_state.user_id = None
            st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

if __name__ == "__main__":
    main()