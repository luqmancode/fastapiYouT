from pydantic import BaseModel, EmailStr, conint
import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostRequest(PostBase):
    pass

# Users
class UserBase(BaseModel):
    email: EmailStr # validate email format with email-validator==2.0.0.post2 library
    password: str


class UserRequest(UserBase):
    pass

class UserResponse(BaseModel):
    id: str
    created_at: datetime.datetime
    email: EmailStr

    class Config:
        orm_mode = True
        
class PostResponse(BaseModel):
    id: str
    created_at: datetime.datetime
    user_id: str
    owner_info: UserResponse

    class Config:
        orm_mode = True

class PostResponseDetail(PostResponse, PostBase):
    pass



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None


class VoteBase(BaseModel):
    post_id: int
    vote_direction: conint(le = 1)
    # user_id: str removing this as we get from current user request

class VoteRequest(VoteBase):
    pass 

class VoteResponse(BaseModel):
    status: str

    class Config:
        orm_model = False

class PostVoteResponse(PostBase):
    Post: PostResponse
    vote_counts: int

    class Config:
        orm_mode = True