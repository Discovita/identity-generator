from typing import Optional, List
from pydantic import Field

from .base import AdaloRecord, GetRecordsResponse


class AdaloIdentity(AdaloRecord):
    Movie_Poster_Moments: Optional[List[int]] = Field(None, alias="Movie Poster Moments")
    User_identity: Optional[List[int]] = Field(None, alias="User identity")
    Shadow_Keepers: Optional[List[int]] = Field(None, alias="Shadow Keepers")
    Actions_incompleted_count: Optional[int] = Field(None, alias="Actions incompleted count")
    Name: Optional[str] = None
    show_shadows: Optional[bool] = Field(None, alias="show shadows, true?")
    Todays_Healthscore: Optional[int] = Field(None, alias="Today's Healthscore")
    Show_I_AM: Optional[bool] = Field(None, alias="Show I AM, true?")
    Order_Number: Optional[int] = Field(None, alias="Order #")
    Safety_phrase: Optional[str] = Field(None, alias="Safety phrase")
    Actions: Optional[List[int]] = None
    AI_Identity_Images: Optional[List[int]] = Field(None, alias="AI Identity Images")
    Actions_completed_count: Optional[int] = Field(None, alias="Actions completed count")
    Show_safety_phrase: Optional[bool] = Field(None, alias="Show, safety phrase, true")
    Health_Score: Optional[int] = Field(None, alias="Health Score")
    I_am_statement: Optional[str] = Field(None, alias="I am statement")


class GetIdentitiesResponse(GetRecordsResponse):
    records: List[AdaloIdentity]
