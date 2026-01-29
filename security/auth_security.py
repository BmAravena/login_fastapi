from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User
from security.auth_hash_password import verify_password
from sqlalchemy.orm import Session


SECRET_KEY = "super_secret_password"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Authentication functions
def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(email: str, password: str, db):
    user = get_user(db, email)
    if not user or not verify_password(password, user.hashed_password):
         return None
    return user

# def authenticate_user(email: str, password: str, db: Session):
#     user = get_user(db, email)
#     if not user:
#         return None
#     if not verify_password(password, user.hashed_password):
#         return None
#     return user



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    
    except JWTError as e:
        #raise Exception(f"No valid token or expired token: {e}")
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Not valid or expired token: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )

