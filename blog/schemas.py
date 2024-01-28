from pydantic import BaseModel
from typing import List,Optional


class BlogBase(BaseModel):
    title: str
    body: str

    class Config():
        from_attributes = True


class Blog(BlogBase):
    class Config():
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config():
        from_attributes = True


class ShowUser(BaseModel):
    id :int
    name: str   
    email: str

    class Config():
        from_attributes = True


class ShowBlog(Blog):
    id :int
    class Config():
        from_attributes = True


class Login(BaseModel):
    username: str
    password:str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    id : Optional[int] = None

