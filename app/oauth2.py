# pip install "python-jose[cryptography]"
# SECRET
# ALGORITHM
# EXPIRATION TIME
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

SECRET_KEY = settings.jwt_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRE_IN_MINUTES = settings.token_expiry_time
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = TOKEN_EXPIRE_IN_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_ = payload.get('user_id')
        if not id_:
            raise credentials_exception
        token_data = schemas.TokenData(user_id = id_)
    except JWTError:
        raise credentials_exception
    return token_data

def get_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    active_user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    return active_user