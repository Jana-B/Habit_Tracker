import bcrypt
from database import User, session

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(username, password):
    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()

def login_user(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None