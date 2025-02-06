from datetime import datetime
from typing import List

from pydantic import BaseModel


class AdaloUser(BaseModel):
    Email: str
    Username: str
    Full_Name: str
    Admin: bool
    Daily_Reminder: bool
    show_identity: bool
    Download_identity_count: int
    Turn_On: datetime
    AI_Image_Copy: str


class GetUsersResponse(BaseModel):
    records: List[AdaloUser]
    offset: int
