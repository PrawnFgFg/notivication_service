from pydantic import BaseModel, EmailStr




class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str

    
class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str
    nickname: str


class UserLoginIn(BaseModel):
    email: EmailStr
    password: str
    
    
class UserPutUpdate(BaseModel):
    nickname: str
    
    
class UserS(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str 
    nickname: str
    role: str
    
class UserSGetMe(BaseModel):
    email: EmailStr
    nickname: str
    role: str