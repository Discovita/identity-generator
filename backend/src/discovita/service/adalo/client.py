from typing import Optional
import json
from contextlib import contextmanager

import httpx

from discovita.config import Settings
from .models import AdaloUser, GetUsersResponse
from .logging import logger

USERS_COLLECTION_ID = "t_8200ffc0140b491aaac8db5b6d8d5ded"

class AdaloClient:
    def __init__(self, app_id: Optional[str] = None, api_key: Optional[str] = None):
        settings = Settings.from_env()
        self.app_id = app_id or settings.adalo_app_id
        self.base_url = f"https://api.adalo.com/v0/apps/{self.app_id}/collections"
        self.headers = {
            "Authorization": f"Bearer {api_key or settings.adalo_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.client = httpx.Client(
            timeout=30.0,  # 30 second timeout
            verify=True,   # Verify SSL certificates
            http2=True    # Enable HTTP/2 for better performance
        )

    def _build_collection_url(self, collection_id: str, element_id: Optional[int] = None) -> str:
        url = f"{self.base_url}/{collection_id}"
        if element_id is not None:
            url = f"{url}/{element_id}"
        return url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_users(self, offset: int = 0, limit: int = 100, email: Optional[str] = None) -> GetUsersResponse:
        url = self._build_collection_url(USERS_COLLECTION_ID)
        params = {
            "offset": offset,
            "limit": limit
        }
        if email:
            params["filterKey"] = "Email"
            params["filterValue"] = email
        
        logger.info(f"Making GET request to {url} with params: {params}")
        response = self.client.get(
            url,
            headers=self.headers,
            params=params
        )
        logger.info(f"Response status: {response.status_code}")
        response.raise_for_status()
        
        response_json = response.json()
        logger.debug(f"Raw API response: {json.dumps(response_json, indent=2)}")
        
        return GetUsersResponse.parse_obj(response_json)

    def create_user(self, user: AdaloUser) -> AdaloUser:
        url = self._build_collection_url(USERS_COLLECTION_ID)
        # Convert to dict and filter out None values
        payload = {k: v for k, v in user.dict(by_alias=True).items() if v is not None}
        logger.debug(f"POST request payload: {json.dumps(payload, indent=2)}")
        
        # Log the raw request for debugging
        logger.debug(f"Request headers: {self.headers}")
        logger.debug(f"Request URL: {url}")
        
        response = self.client.post(
            url,
            headers=self.headers,
            json=payload
        )
        
        if response.status_code != 200:
            logger.error(f"API error response: {response.text}")
            logger.error(f"Response headers: {response.headers}")
        response.raise_for_status()
        
        return AdaloUser.parse_obj(response.json())

    def get_user(self, user_id: int) -> AdaloUser:
        url = self._build_collection_url(USERS_COLLECTION_ID, user_id)
        response = self.client.get(url, headers=self.headers)
        response.raise_for_status()
        
        return AdaloUser.parse_obj(response.json())
