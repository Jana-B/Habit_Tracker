import os
import cloudinary.uploader
from dotenv import load_dotenv
from db import get_user_collection
import streamlit as st

# Load environment variables
load_dotenv()

# Cloudinary setup
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_profile_image(image, username):
    # Upload image to Cloudinary
    upload_result = cloudinary.uploader.upload(image)
    image_url = upload_result['url']

    # Save image URL to the database
    users = get_user_collection()
    users.update_one({"username": username}, {"$set": {"profile_image_url": image_url}})
    
    return image_url

def get_profile_image(username):
    # Retrieve user's profile image from the database
    users = get_user_collection()
    user = users.find_one({"username": username})
    return user.get("profile_image_url")