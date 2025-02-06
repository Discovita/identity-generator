from typing import Optional

import httpx

from models import AdaloUser, GetUsersResponse

USERS_COLLECTION_ID = "t_8200ffc0140b491aaac8db5b6d8d5ded"

class AdaloClient:
    def __init__(self, app_id: str, api_key: str):
        self.app_id = app_id
        self.base_url = f"https://api.adalo.com/v0/apps/{app_id}/collections"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _build_collection_url(self, collection_id: str, element_id: Optional[int] = None) -> str:
        url = f"{self.base_url}/{collection_id}"
        if element_id is not None:
            url = f"{url}/{element_id}"
        return url

    def get_users(self, offset: int = 0, limit: int = 100) -> GetUsersResponse:
        url = self._build_collection_url(USERS_COLLECTION_ID)
        response = httpx.get(
            url,
            headers=self.headers,
            params={"offset": offset, "limit": limit}
        )
        response.raise_for_status()
        
        return GetUsersResponse.parse_obj(response.json())

    def create_user(self, user: AdaloUser) -> AdaloUser:
        url = self._build_collection_url(USERS_COLLECTION_ID)
        response = httpx.post(
            url,
            headers=self.headers,
            json=user.dict()
        )
        response.raise_for_status()
        
        return AdaloUser.parse_obj(response.json())

    def get_user(self, user_id: int) -> AdaloUser:
        url = self._build_collection_url(USERS_COLLECTION_ID, user_id)
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()
        
        return AdaloUser.parse_obj(response.json())
