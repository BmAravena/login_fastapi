from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas
from database_connection import sessionLocal, engine
from models import Base

#Base.metadata.create_all(bind=engine) # for local database


# Create database and tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependence to get database Session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    return db_user