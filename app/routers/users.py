# Users
from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, database, utils, models
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix = '/users', tags = ['users']
)

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
async def register_user(user: schemas.UserRequest, db: Session = Depends(database.get_db)):
    user_dict = user.dict()
    exist_user = db.query(models.User).filter(models.User.email == user_dict.get('email')).first()
    if exist_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Email already exists")
    user_dict['password'] = utils.get_password_hash(user_dict['password'])
    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get('/', response_model = List[schemas.UserResponse])
async def get_users(db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).all()
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No more users created")
    return db_user

@router.get('/{id}', response_model = schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid User {id}")
    return db_user
