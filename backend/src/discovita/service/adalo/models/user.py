from typing import Optional, List
from pydantic import Field

from .base import AdaloRecord, GetRecordsResponse


class ProfilePhoto(AdaloRecord):
    url: str
    size: int
    width: int
    height: int
    filename: str


class AdaloUser(AdaloRecord):
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


class GetUsersResponse(GetRecordsResponse):
    records: List[AdaloUser]
