from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import utils, schemas, oauth2
from database import get_db
from models import User

router = APIRouter(
    prefix='',
    tags=['Auth']
)

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credential")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credential")

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}