from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserProfileBase(BaseModel):
    bio: Optional[str] = ""
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    theme_preference: str = "light"
    language: str = "zh-CN"
    notification_preferences: Optional[dict] = {}


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class User(UserBase):
    id: Optional[int] = None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserProfile(UserProfileBase):
    id: Optional[int] = None
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str