from typing import Optional
from contextlib import contextmanager

from .base import BaseAdaloClient
from .users import UsersClient
from .identities import IdentitiesClient
from ..models.user import AdaloUser, GetUsersResponse
from ..models.identity import AdaloIdentity, GetIdentitiesResponse


class AdaloClient:
    def __init__(self, app_id: Optional[str] = None, api_key: Optional[str] = None):
        self._users = UsersClient(app_id, api_key)
        self._identities = IdentitiesClient(app_id, api_key)

    def __enter__(self):
        self._users.__enter__()
        self._identities.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._users.__exit__(exc_type, exc_val, exc_tb)
        self._identities.__exit__(exc_type, exc_val, exc_tb)

    # Users operations
    def get_users(self, offset: int = 0, limit: int = 100, email: Optional[str] = None) -> GetUsersResponse:
        return self._users.get_users(offset, limit, email)

    def create_user(self, user: AdaloUser) -> AdaloUser:
        return self._users.create_user(user)

    def get_user(self, user_id: int) -> AdaloUser:
        return self._users.get_user(user_id)

    def update_user(self, user_id: int, user: AdaloUser) -> AdaloUser:
        return self._users.update_user(user_id, user)

    def delete_user(self, user_id: int) -> None:
        return self._users.delete_user(user_id)

    # Identities operations
    def get_identities(self, offset: int = 0, limit: int = 100) -> GetIdentitiesResponse:
        return self._identities.get_identities(offset, limit)

    def create_identity(self, identity: AdaloIdentity) -> AdaloIdentity:
        return self._identities.create_identity(identity)

    def get_identity(self, identity_id: int) -> AdaloIdentity:
        return self._identities.get_identity(identity_id)

    def update_identity(self, identity_id: int, identity: AdaloIdentity) -> AdaloIdentity:
        return self._identities.update_identity(identity_id, identity)

    def delete_identity(self, identity_id: int) -> None:
        return self._identities.delete_identity(identity_id)


__all__ = [
    "BaseAdaloClient",
    "UsersClient",
    "IdentitiesClient",
    "AdaloClient"
]
