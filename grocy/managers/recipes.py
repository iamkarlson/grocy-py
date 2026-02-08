from __future__ import annotations

from typing import TYPE_CHECKING

from ..data_models.meal_items import RecipeItem

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class RecipeManager:
    """Manage recipes and their fulfillment status.

    Access via ``grocy.recipes``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def get(self, recipe_id: int) -> RecipeItem | None:
        """Get a single recipe by ID."""
        recipe = self._api.get_recipe(recipe_id)
        if recipe:
            return RecipeItem.from_response(recipe)
        return None

    def consume(self, recipe_id: int):
        """Consume all ingredients of a recipe from stock."""
        return self._api.consume_recipe(recipe_id)

    def fulfillment(self, recipe_id: int):
        """Get the fulfillment status of a recipe."""
        return self._api.get_recipe_fulfillment(recipe_id)

    def all_fulfillment(self):
        """Get the fulfillment status of all recipes."""
        return self._api.get_all_recipes_fulfillment()

    def copy(self, recipe_id: int):
        """Create a copy of a recipe."""
        return self._api.copy_recipe(recipe_id)

    def add_not_fulfilled_to_shopping_list(self, recipe_id: int):
        """Add unfulfilled recipe ingredients to the shopping list."""
        return self._api.add_not_fulfilled_to_shopping_list(recipe_id)
