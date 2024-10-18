import streamlit as st
from auth import login_user, register_user
from dashboard import dashboard_tab
from habits import habit_tab
from userprofile import profile_tab

# Mockup for user session, replace this with a real authentication system later.
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

# Sidebar navigation
def main():
    st.sidebar.title("Habit Tracker")

    if st.session_state["user_id"]:
        # User is logged in, show tabs
        tabs = ["Dashboard", "Habits", "Profile"]
        choice = st.sidebar.radio("Navigate", tabs)

        if choice == "Dashboard":
            st.title("Dashboard")
            dashboard_tab(st.session_state["user_id"])
        elif choice == "Habits":
            st.title("Manage Habits")
            habit_tab(st.session_state["user_id"])
        elif choice == "Profile":
            st.title("User Profile")
            profile_tab(st.session_state["user_id"])

    else:
        # If no user is logged in, show login/register options
        st.sidebar.subheader("Login / Register")
        auth_choice = st.sidebar.selectbox("Choose action", ["Login", "Register"])

    if auth_choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = login_user(username, password)
            if "user_id" in user:  # Check if 'user_id' is returned
                st.session_state["user_id"] = user["user_id"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(user.get("error", "Unknown error occurred!"))

        elif auth_choice == "Register":
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Register"):
                register_user(username, password)
                st.success("User registered! Please login.")

if __name__ == '__main__':
    main()