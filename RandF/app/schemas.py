
# 1. Defining pydantic classes for data authentication


from pydantic import BaseModel
from typing import Optional
from enum import Enum

# Defining the level only
class UserLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"
    
# this contains the data of user
class UserBase(BaseModel):
    email: str
    username: str
    age:Optional[int] = None
    level :UserLevel = UserLevel.beginner

#this contains the password enterd by the users
class UserIn(UserBase):
    password:str
    
class UserInDBBase(UserBase):
    id: int
    class Config: 
        orm_mode = True

# this contains password of the database
class UserInDB(UserInDBBase):
    hashed_password:str


#information to be stored in the jwt. Do not store 
# information like passwords here.
class TokenData(BaseModel):
    username: Optional[str] = None
  
# This is token  
class Token(BaseModel):
    access_token :str
    token_type :str