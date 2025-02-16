from typing import Optional

from .base import BaseAdaloClient
from ..models.identity import AdaloIdentity, GetIdentitiesResponse

IDENTITIES_COLLECTION_ID = "t_0lnnuplpppxwik9nor4e5n5w7"

class IdentitiesClient(BaseAdaloClient[AdaloIdentity, GetIdentitiesResponse]):
    def __init__(self, app_id: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(
            collection_id=IDENTITIES_COLLECTION_ID,
            record_type=AdaloIdentity,
            response_type=GetIdentitiesResponse,
            app_id=app_id,
            api_key=api_key
        )

    def get_identities(self, offset: int = 0, limit: int = 100) -> GetIdentitiesResponse:
        return self.get_records(offset, limit)

    def create_identity(self, identity: AdaloIdentity) -> AdaloIdentity:
        return self.create_record(identity)

    def get_identity(self, identity_id: int) -> AdaloIdentity:
        return self.get_record(identity_id)

    def update_identity(self, identity_id: int, identity: AdaloIdentity) -> AdaloIdentity:
        return self.update_record(identity_id, identity)

    def delete_identity(self, identity_id: int) -> None:
        return self.delete_record(identity_id)
