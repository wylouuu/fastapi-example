from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        from_attributes = True
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner: UserOut
    created_at: datetime
    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le = 1)
    
class VoteCreate(BaseModel):
    post_id: int
    user_id: int