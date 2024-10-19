import streamlit as st
import cloudinary
import cloudinary.uploader
from db import get_user_collection

def show_profile(user):
    st.header("Profile")

    st.subheader(f"Username: {user['username']}")
    
    # Profile Image Upload
    st.subheader("Upload Profile Picture")
    uploaded_file = st.file_uploader("Choose a file")
    
    if uploaded_file:
        result = cloudinary.uploader.upload(uploaded_file, folder="profile_pictures")
        image_url = result.get("url")
        
        user_collection = get_user_collection()
        user_collection.update_one({"_id": user['_id']}, {"$set": {"profile_image": image_url}})
        st.success("Profile picture updated!")
        st.image(image_url, width=200)