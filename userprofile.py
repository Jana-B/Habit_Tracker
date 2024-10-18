import streamlit as st
import cloudinary
import cloudinary.uploader
import os
from database import get_users_collection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Cloudinary credentials
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def manage_profile(user_data):
    st.header("Profile")
    st.write(f"Username: {user_data['username']}")

    # Display the existing profile picture if available
    if 'profile_picture' in user_data:
        st.image(user_data['profile_picture'], width=150)  # Display existing profile picture

    # Profile picture upload (using Cloudinary)
    st.subheader("Update Profile Picture")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Upload the file to Cloudinary
        try:
            cloudinary_response = cloudinary.uploader.upload(uploaded_file)
            cloudinary_url = cloudinary_response['secure_url']

            # Update the user's profile picture in the database
            get_users_collection().update_one(
                {"_id": user_data['_id']},
                {"$set": {"profile_picture": cloudinary_url}}
            )

            st.success("Profile picture updated!")
            st.image(cloudinary_url, width=150)  # Display newly uploaded image

        except Exception as e:
            st.error(f"An error occurred while uploading the image: {str(e)}")
    else:
        st.info("No file uploaded yet")