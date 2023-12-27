from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session

import models, schemas, oauth2
from database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('', status_code = status.HTTP_200_OK, response_model = list[schemas.Post])
def read_all_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)
    return posts

@router.get('/{id}', status_code = status.HTTP_200_OK, response_model = schemas.Post)
def read_a_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    return post

@router.post('', status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    post_query.delete(synchronize_session=False)
    db.commit()

    return

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model = schemas.Post)
def update_a_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()