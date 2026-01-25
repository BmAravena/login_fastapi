from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User
from security.auth_hash_password import verify_password

SECRET_KEY = "super_secret_password"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Authentication functions
def get_user(db, username: str):
    user_dict = db.get(username)
    if user_dict:
        return User(**user_dict)
    

def authenticate_user(username: str, password: str, db):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user