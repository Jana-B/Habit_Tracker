# userprofile.py
import streamlit as st
from database import get_users_collection

def manage_profile(user_data):
    st.header("Profile")
    st.write(f"Username: {user_data['username']}")

    # Profile picture upload (using Cloudinary or another service)
    st.subheader("Update Profile Picture")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Here you would upload the file to Cloudinary and save the URL to MongoDB
        # For example:
        # cloudinary_url = upload_to_cloudinary(uploaded_file)
        # get_users_collection().update_one({"_id": user_data['_id']}, {"$set": {"profile_picture": cloudinary_url}})
        st.success("Profile picture updated!")  # After updating, show success
    else:
        st.info("No file uploaded yet")