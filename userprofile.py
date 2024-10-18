import streamlit as st
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from database import db
from models import User
import os

# Load Cloudinary credentials from .env
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")

def upload_profile_pic(file):
    """Uploads an image file to Cloudinary."""
    result = upload(file, folder="profile_pics", cloud_name=CLOUDINARY_CLOUD_NAME)
    return result['secure_url']

def profile_tab(user_id):
    user = User(db)
    user_data = user.find_user_by_id(user_id)

    st.subheader("Your Profile")
    
    # Display current profile picture
    if user_data.get("profile_pic"):
        st.image(user_data["profile_pic"], width=150)

    # Profile picture upload
    uploaded_file = st.file_uploader("Upload a new profile picture", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        pic_url = upload_profile_pic(uploaded_file)
        user.update_profile_pic(user_id, pic_url)
        st.success("Profile picture updated!")
        st.rerun()  # Rerun to show updated picture

    st.write(f"**Username:** {user_data['username']}")