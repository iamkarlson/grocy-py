from __future__ import annotations

from typing import TYPE_CHECKING

from ..data_models.meal_items import MealPlanItem, MealPlanSection

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class MealPlanManager:
    """Manage meal plan entries and sections.

    Access via ``grocy.meal_plan``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def items(
        self, get_details: bool = False, query_filters: list[str] | None = None
    ) -> list[MealPlanItem]:
        """Get all meal plan items.

        Args:
            get_details: Fetch recipe and section details for each item.
            query_filters: Optional Grocy API query filters.
        """
        raw = self._api.get_meal_plan(query_filters)
        meal_plan = [MealPlanItem.from_response(data) for data in raw]
        if get_details:
            for item in meal_plan:
                item.get_details(self._api)
        return meal_plan

    def sections(self, query_filters: list[str] | None = None) -> list[MealPlanSection]:
        """Get all meal plan sections."""
        raw = self._api.get_meal_plan_sections(query_filters)
        return [MealPlanSection.from_response(section) for section in raw]

    def section(self, section_id: int) -> MealPlanSection | None:
        """Get a single meal plan section by ID."""
        section = self._api.get_meal_plan_section(section_id)
        if section:
            return MealPlanSection.from_response(section)
        return None
