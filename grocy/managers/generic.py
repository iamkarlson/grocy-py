from __future__ import annotations

from typing import TYPE_CHECKING

from ..data_models.generic import EntityType

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class GenericEntityManager:
    """Perform CRUD operations on any Grocy entity type.

    Access via ``grocy.generic``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def list(
        self, entity_type: EntityType, query_filters: list[str] | None = None
    ) -> list[dict]:
        """List all objects of a given entity type.

        Args:
            entity_type: The Grocy entity type.
            query_filters: Optional Grocy API query filters.
        """
        return (
            self._api.get_generic_objects_for_type(entity_type.value, query_filters)
            or []
        )

    def get(self, entity_type: EntityType, object_id: int) -> dict:
        """Get a single object by entity type and ID."""
        return self._api.get_generic(entity_type.value, object_id)

    def create(self, entity_type: EntityType, data) -> dict:
        """Create a new object of a given entity type.

        Args:
            entity_type: The Grocy entity type.
            data: Object fields.
        """
        return self._api.add_generic(entity_type.value, data)

    def update(self, entity_type: EntityType, object_id: int, data):
        """Update an existing object.

        Args:
            entity_type: The Grocy entity type.
            object_id: The object ID.
            data: Fields to update.
        """
        return self._api.update_generic(entity_type.value, object_id, data)

    def delete(self, entity_type: EntityType, object_id: int):
        """Delete an object by entity type and ID."""
        return self._api.delete_generic(entity_type.value, object_id)

    def get_userfields(self, entity: str, object_id: int):
        """Get custom userfields for an entity object.

        Args:
            entity: The entity type name string.
            object_id: The object ID.
        """
        return self._api.get_userfields(entity, object_id)

    def set_userfields(self, entity: str, object_id: int, key: str, value):
        """Set a custom userfield value for an entity object.

        Args:
            entity: The entity type name string.
            object_id: The object ID.
            key: The userfield key.
            value: The userfield value.
        """
        return self._api.set_userfields(entity, object_id, key, value)
