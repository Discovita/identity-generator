from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class ProfilePhoto(BaseModel):
    url: str
    size: int
    width: int
    height: int
    filename: str


class AdaloUser(BaseModel):
    id: Optional[int] = None
    Email: Optional[str] = None
    Username: Optional[str] = None
    Password: Optional[str] = None
    Profile_Photo: Optional[ProfilePhoto] = Field(None, alias="Profile Photo")
    Full_Name: Optional[str] = Field(None, alias="Full Name")
    AI_Image_Copy: Optional[str] = Field(None, alias="AI Image Copy")
    Admin: Optional[bool] = None
    show_identity: Optional[bool] = Field(None, alias="show identity, true?")
    AI_generated_profile_pic: Optional[str] = Field(None, alias="AI generated profile pic")
    Daily_Reminder: Optional[bool] = Field(None, alias="Daily Reminder, true")
    Turn_On: Optional[str] = Field(None, alias="Turn On")
    Download_identity_count: Optional[int] = Field(None, alias="Download identity count.")
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        extra = "allow"
        populate_by_name = True


class GetUsersResponse(BaseModel):
    records: List[AdaloUser]
    offset: int = 0

    class Config:
        extra = "allow"
