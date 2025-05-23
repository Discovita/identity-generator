from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AdaloRecord(BaseModel):
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        extra = "allow"
        populate_by_name = True


class GetRecordsResponse(BaseModel):
    offset: int = 0

    class Config:
        extra = "allow"
