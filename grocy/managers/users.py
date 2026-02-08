from __future__ import annotations

from typing import TYPE_CHECKING

from ..data_models.user import User

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class UserManager:
    """Manage Grocy users, settings, and permissions.

    Access via ``grocy.users``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def list(self) -> list[User]:
        """Get all users."""
        user_dtos = self._api.get_users()
        return [
            User(
                id=u.id,
                username=u.username,
                first_name=u.first_name,
                last_name=u.last_name,
                display_name=u.display_name,
            )
            for u in user_dtos
        ]

    def get(self, user_id: int) -> User | None:
        """Get a single user by ID."""
        user = self._api.get_user(user_id=user_id)
        if user:
            return User(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                display_name=user.display_name,
            )
        return None

    def current(self) -> User | None:
        """Get the currently authenticated user."""
        user = self._api.get_current_user()
        if user:
            return User(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                display_name=user.display_name,
            )
        return None

    def create(self, data: dict):
        """Create a new user.

        Args:
            data: User fields as a dictionary.
        """
        return self._api.create_user(data)

    def edit(self, user_id: int, data: dict):
        """Edit an existing user.

        Args:
            user_id: The Grocy user ID.
            data: Fields to update.
        """
        return self._api.edit_user(user_id, data)

    def delete(self, user_id: int):
        """Delete a user."""
        return self._api.delete_user(user_id)

    def settings(self):
        """Get all settings for the current user."""
        return self._api.get_user_settings()

    def get_setting(self, key: str):
        """Get a single user setting by key."""
        return self._api.get_user_setting(key)

    def set_setting(self, key: str, value):
        """Set a user setting.

        Args:
            key: The setting key.
            value: The setting value.
        """
        return self._api.set_user_setting(key, value)

    def delete_setting(self, key: str):
        """Delete a user setting."""
        return self._api.delete_user_setting(key)
