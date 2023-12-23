from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('', status_code = status.HTTP_200_OK, response_model = list[schemas.Post])
def read_all_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get('/{id}', status_code = status.HTTP_200_OK, response_model = schemas.Post)
def read_all_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    return post

@router.post('', status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
