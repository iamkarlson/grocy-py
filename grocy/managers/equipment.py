from __future__ import annotations

from typing import TYPE_CHECKING

from ..data_models.equipment import Equipment
from ..data_models.generic import EntityType
from ..grocy_api_client import EquipmentData

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class EquipmentManager:
    """Manage equipment items and their details.

    Access via ``grocy.equipment``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def list(
        self, query_filters: list[str] | None = None, get_details: bool = False
    ) -> list[Equipment]:
        """Get all equipment items.

        Args:
            query_filters: Optional Grocy API query filters.
            get_details: Fetch full details for each item.
        """
        raw_equipment = self._api.get_all_equipment(query_filters)
        equipment_items = [Equipment.from_dict(item) for item in raw_equipment]
        if get_details:
            for item in equipment_items:
                item.get_details(self._api)
        return equipment_items

    def get(self, equipment_id: int) -> Equipment | None:
        """Get a single equipment item by ID."""
        equipment_data = self._api.get_equipment(equipment_id)
        if equipment_data:
            return Equipment.from_details_response(equipment_data)
        return None

    def get_by_name(self, name: str) -> Equipment | None:
        """Get a single equipment item by name."""
        query_filters = [f"name={name}"]
        equipment_items = self.list(query_filters, True)
        if equipment_items and len(equipment_items) > 0:
            return equipment_items[0]
        return None

    def get_all_objects(self) -> list[Equipment]:
        """Get all equipment items with full details fetched from the API."""
        raw_equipment = self._api.get_generic_objects_for_type(EntityType.EQUIPMENT)
        if not raw_equipment:
            return []
        equipment_data = [EquipmentData(**eq) for eq in raw_equipment]
        equipment_items = []
        for item in equipment_data:
            equipment_details = self._api.get_equipment(item.id)
            if equipment_details:
                equipment_items.append(
                    Equipment.from_details_response(equipment_details)
                )
        return equipment_items
