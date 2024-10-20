from datetime import datetime
import streamlit as st
from auth import register_user, login_user, logout_user
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
            name = st.text_input("Habit Name")
            color = st.color_picker("Habit Color", "#00f900")
            if st.button("Create Habit"):
                create_habit(name, color, st.session_state["username"])
                st.success("Habit created successfully!")
                st.rerun()  # Refresh page after creating habit

            # Display User's Habits
            st.subheader("Your Habits")
            habits = get_user_habits(st.session_state["username"])
            today = datetime.now().strftime("%Y-%m-%d")

            for habit in habits:
                st.write(f"**{habit['name']}**")
                
                # Ensure the habit has an entry for today
                add_entry_if_missing(habit["_id"], today)
                
                # Find today's entry
                today_entry = next((entry for entry in habit["entries"] if entry["date"] == today), {"value": 0})
                
                st.write(f"Today's Progress: {today_entry['value']}")
                
                # Increment and Decrement buttons
                if st.button(f"Increase ({habit['name']})", key=f"inc_{habit['_id']}"):
                    increment_habit(habit["_id"], today)
                    st.rerun()  # Refresh page after incrementing
                
                if st.button(f"Decrease ({habit['name']})", key=f"dec_{habit['_id']}"):
                    decrement_habit(habit["_id"], today)
                    st.rerun()  # Refresh page after decrementing

                # Edit Habit Name
                new_name = st.text_input(f"Edit Habit Name ({habit['name']})", value=habit["name"], key=f"edit_{habit['_id']}")
                if st.button(f"Update Habit ({habit['name']})", key=f"update_{habit['_id']}"):
                    update_habit_name(habit["_id"], new_name)
                    st.success(f"Habit '{habit['name']}' updated!")
                    st.rerun()  # Refresh page after updating

                # Delete Habit
                if st.button(f"Delete Habit ({habit['name']})", key=f"del_{habit['_id']}"):
                    delete_habit(habit["_id"])
                    st.warning(f"Habit '{habit['name']}' deleted!")
                    st.rerun()  # Refresh page after deleting

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