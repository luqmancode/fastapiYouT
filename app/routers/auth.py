from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, utils, oauth2
router = APIRouter(tags = ['authentication'])

@router.post('/login', response_model = schemas.LoginResponse)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not db_user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")
    if not utils.verify_password(user_credentials.password, db_user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")
    
    # create token
    access_token = oauth2.create_token({"user_id": db_user.id})
    user_expire_token = {"access_token": access_token, "token_type": "bearer"}
    return user_expire_token

    