from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session

import models, schemas, utils
from database import get_db

router = APIRouter()

@router.get('/users', status_code = status.HTTP_200_OK, response_model = list[schemas.User])
def read_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users

@router.get('/users/{id}', status_code=status.HTTP_200_OK, response_model = schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user

@router.post('/users', status_code = status.HTTP_201_CREATED, response_model = schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
