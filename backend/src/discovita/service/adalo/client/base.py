from typing import Optional, TypeVar, Generic, Type
import json
from contextlib import contextmanager

import httpx

from discovita.config import Settings
from ..models.base import AdaloRecord, GetRecordsResponse
from ..logging import logger

T = TypeVar('T', bound=AdaloRecord)
R = TypeVar('R', bound=GetRecordsResponse)

class BaseAdaloClient(Generic[T, R]):
    def __init__(
        self, 
        collection_id: str,
        record_type: Type[T],
        response_type: Type[R],
        app_id: Optional[str] = None, 
        api_key: Optional[str] = None
    ):
        settings = Settings.from_env()
        self.app_id = app_id or settings.adalo_app_id
        self.collection_id = collection_id
        self.record_type = record_type
        self.response_type = response_type
        self.base_url = f"https://api.adalo.com/v0/apps/{self.app_id}/collections"
        self.headers = {
            "Authorization": f"Bearer {api_key or settings.adalo_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.client = httpx.Client(
            timeout=30.0,
            verify=True,
            http2=True
        )

    def _build_collection_url(self, element_id: Optional[int] = None) -> str:
        url = f"{self.base_url}/{self.collection_id}"
        if element_id is not None:
            url = f"{url}/{element_id}"
        return url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_records(
        self, 
        offset: int = 0, 
        limit: int = 100, 
        filter_key: Optional[str] = None,
        filter_value: Optional[str] = None
    ) -> R:
        url = self._build_collection_url()
        params: dict[str, str | int] = {
            "offset": str(offset),
            "limit": str(limit)
        }
        if filter_key and filter_value:
            params["filterKey"] = filter_key
            params["filterValue"] = filter_value
        
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
        
        return self.response_type.parse_obj(response_json)

    def create_record(self, record: T) -> T:
        url = self._build_collection_url()
        payload = {k: v for k, v in record.dict(by_alias=True).items() if v is not None}
        logger.debug(f"POST request payload: {json.dumps(payload, indent=2)}")
        
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
        
        return self.record_type.parse_obj(response.json())

    def get_record(self, record_id: int) -> T:
        url = self._build_collection_url(record_id)
        response = self.client.get(url, headers=self.headers)
        response.raise_for_status()
        
        return self.record_type.parse_obj(response.json())

    def update_record(self, record_id: int, record: T) -> T:
        url = self._build_collection_url(record_id)
        payload = {k: v for k, v in record.dict(by_alias=True).items() if v is not None}
        
        response = self.client.put(
            url,
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        return self.record_type.parse_obj(response.json())

    def delete_record(self, record_id: int) -> None:
        url = self._build_collection_url(record_id)
        response = self.client.delete(url, headers=self.headers)
        response.raise_for_status()
