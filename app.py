from datetime import datetime
import streamlit as st
from auth import register_user, login_user, logout_user
from db import create_unique_username_index
from habit import create_habit, get_user_habits, update_habit_name, delete_habit, decrement_habit, increment_habit, add_entry_if_missing
from userprofile import upload_profile_image, get_profile_image
from dashboard import display_dashboard
from bson import ObjectId

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["page"] = "Login"  # Default to Login page

# Sidebar for navigation and profile image
def render_sidebar():
    with st.sidebar:
        st.title("Habit Tracker")
        if st.session_state["logged_in"]:
            username = st.session_state["username"]
            profile_image = get_profile_image(username)
            
            if profile_image:
                st.image(profile_image, width=50)  # Display small version of the profile picture
            
            st.write(f"Welcome, {username}!")
            page = st.radio("Navigate", ["Dashboard", "Habits", "Profile"])
            st.button("Logout", on_click=logout_user)
        else:
            page = st.radio("Navigate", ["Login", "Register"])
    return page

# Main app logic
def main():
    create_unique_username_index()
    page = render_sidebar()

    if page == "Register":
        st.title("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            success, message = register_user(username, password)
            if success:
                st.success(message)
            else:
                st.error(message)

    elif page == "Login":
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, message = login_user(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["page"] = "Dashboard"  # Redirect to dashboard
                st.rerun()  # Trigger rerun to display Dashboard
            else:
                st.error(message)

    elif st.session_state["logged_in"]:
        if page == "Dashboard":
            display_dashboard(st.session_state["username"])

        elif page == "Habits":
            st.title("Manage Habits")
            
            # Habit Creation
            with st.form(key='create_habit'):
                col1, col2 = st.columns([3, 1])
                with col1:
                    name = st.text_input("Habit Name")
                with col2:
                    color = st.color_picker("Color", "#00f900")
                submit_button = st.form_submit_button(label="Create Habit")
                if submit_button:
                    create_habit(name, color, st.session_state["username"])
                    st.success("Habit created successfully!")
                    st.rerun()  # Refresh page after creating habit

            # Display User's Habits
            st.subheader("Your Habits")
            habits = get_user_habits(st.session_state["username"])
            today = datetime.now().strftime("%Y-%m-%d")

            for habit in habits:
                with st.expander(f"**{habit['name']}**", expanded=True):
                    # Ensure the habit has an entry for today
                    add_entry_if_missing(habit["_id"], today)
                    
                    # Find today's entry
                    today_entry = next((entry for entry in habit["entries"] if entry["date"] == today), {"value": 0})
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"<p style='color:{habit['color']};'>Today's Progress: {today_entry['value']}</p>", unsafe_allow_html=True)
                    with col2:
                        if st.button("➕", key=f"inc_{habit['_id']}"):
                            increment_habit(habit["_id"], today)
                            st.rerun()
                    with col3:
                        if st.button("➖", key=f"dec_{habit['_id']}"):
                            decrement_habit(habit["_id"], today)
                            st.rerun()

                    # Edit and Delete options
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("New name", value=habit["name"], key=f"edit_{habit['_id']}")
                        if st.button("✏️ Update", key=f"update_{habit['_id']}"):
                            update_habit_name(habit["_id"], new_name)
                            st.success(f"Habit updated!")
                            st.rerun()
                    with col2:
                        st.write("") # For alignment
                        st.write("")
                        if st.button("🗑️ Delete", key=f"del_{habit['_id']}"):
                            delete_habit(habit["_id"])
                            st.warning(f"Habit deleted!")
                            st.rerun()

        elif page == "Profile":
            st.title("Profile")
            username = st.session_state["username"]
            profile_image = get_profile_image(username)

            if profile_image:
                st.image(profile_image, width=150)  # Display the profile picture on the profile page

            image = st.file_uploader("Upload Profile Image", type=["jpg", "png"])
            if image and st.button("Upload"):
                upload_profile_image(image, username)
                st.success("Profile image updated!")
                st.rerun()  # Refresh the page to show the updated profile image

if __name__ == "__main__":
    main()