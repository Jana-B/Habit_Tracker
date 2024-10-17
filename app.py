import streamlit as st
from auth import register_user, login_user
from database import User, session

def main():
    st.title("Habit Tracker")

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    if st.session_state.user_id is None:
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            st.header("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user = login_user(username, password)
                if user:
                    st.session_state.user_id = user.id
                    st.success("Logged in successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")

        with tab2:
            st.header("Register")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            if st.button("Register"):
                if new_username and new_password:
                    try:
                        register_user(new_username, new_password)
                        st.success("Registration successful! Please log in.")
                    except:
                        st.error("Username already exists")
                else:
                    st.error("Please enter both username and password")

    else:
        user = session.query(User).get(st.session_state.user_id)
        st.write(f"Welcome, {user.username}!")
        if st.button("Logout"):
            st.session_state.user_id = None
            st.experimental_rerun()

        # Add habit tracking functionality here

if __name__ == "__main__":
    main()