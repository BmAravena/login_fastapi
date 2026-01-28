from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from security.auth_security import decode_token, get_user, oauth2_scheme
from schemas import UserOut
from database_connection import sessionLocal, engine



# Dependence to get database Session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



def auth():
    pass