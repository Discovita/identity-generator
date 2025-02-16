from typing import Optional

from .base import BaseAdaloClient
from ..models.user import AdaloUser, GetUsersResponse

USERS_COLLECTION_ID = "t_8200ffc0140b491aaac8db5b6d8d5ded"

class UsersClient(BaseAdaloClient[AdaloUser, GetUsersResponse]):
    def __init__(self, app_id: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(
            collection_id=USERS_COLLECTION_ID,
            record_type=AdaloUser,
            response_type=GetUsersResponse,
            app_id=app_id,
            api_key=api_key
        )

    def get_users(self, offset: int = 0, limit: int = 100, email: Optional[str] = None) -> GetUsersResponse:
        return self.get_records(offset, limit, "Email", email)

    def create_user(self, user: AdaloUser) -> AdaloUser:
        return self.create_record(user)

    def get_user(self, user_id: int) -> AdaloUser:
        return self.get_record(user_id)

    def update_user(self, user_id: int, user: AdaloUser) -> AdaloUser:
        return self.update_record(user_id, user)

    def delete_user(self, user_id: int) -> None:
        return self.delete_record(user_id)
