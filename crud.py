from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException
from security.auth_hash_password import hash_password
#from database_connection import sesion


# Users
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users_safe(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    for user in users:
        return[user.email, user.items]

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
 

def create_user(db: Session, user: schemas.UserCreate):
    #fake_hashed_password = user.password + "notreallyhashed"
    print(user.password)
    print("LENGTH:", len(user.password.encode("utf-8")))
    real_hashed_password = hash_password(user.password)

    db_user = models.User(email=user.email, hashed_password=real_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def disable_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    
    db_user.is_active = False
