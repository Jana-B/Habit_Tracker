import bcrypt
from database import get_users_collection
from models import User

# Password hashing function
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Password verification function
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# User registration function
def register_user(username, password):
    users_collection = get_users_collection()
    
    # Check if the user already exists
    if users_collection.find_one({"username": username}):
        return {"error": "User already exists"}
    
    # Hash the password and create a new user
    hashed_password = hash_password(password)
    user = User(users_collection)
    
    result = user.create_user(username, hashed_password)
    
    if result.inserted_id:
        return {"success": "User registered successfully"}
    else:
        return {"error": "Registration failed"}

# User login function
def login_user(username, password):
    users_collection = get_users_collection()
    user = User(users_collection)
    
    # Find user by username
    user_data = user.find_user_by_username(username)
    
    if user_data and verify_password(password, user_data['hashed_password']):
        return {"success": "Login successful", "user_id": str(user_data['_id'])}
    else:
        return {"error": "Invalid username or password"}