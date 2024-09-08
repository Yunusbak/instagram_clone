import uuid

from pydantic import BaseModel
from typing import Optional
from pydantic.types import UUID4


#
class Settings(BaseModel):
    authjwt_secret_key : str = '7d443422712d1f41c22fa5f6de9f754c18d16e430be33e8fb6489c8145887a09'




# User Register #

class UserRegister(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    username: Optional[str]

class UserLogin(BaseModel):
    username : Optional[str]
    password: Optional[str]

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    updated_at: Optional[str]

class UserUpdatePassword(BaseModel):
    password: Optional[str]
    password1: Optional[str]
    password2: Optional[str]




# Post #
class PostCreate(BaseModel):
    image_path: Optional[str]
    caption: Optional[str]

class PostUpdateModel(BaseModel):
    caption: Optional[str]
    image_path: Optional[str]


# Like #

class LikeCreateModel(BaseModel):
    post_id : Optional[uuid.UUID]


# Comment #

class CommentCreateSchema(BaseModel):
    post_id : Optional[uuid.UUID]
    content: Optional[str]

class CommentUpdateSchema(BaseModel):
    content: Optional[str]