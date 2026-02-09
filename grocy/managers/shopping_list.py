from __future__ import annotations

from typing import TYPE_CHECKING

from ..data_models.product import ShoppingListProduct

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class ShoppingListManager:
    """Manage shopping lists and their items.

    Access via ``grocy.shopping_list``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def items(
        self, get_details: bool = False, query_filters: list[str] | None = None
    ) -> list[ShoppingListProduct]:
        """Get all items on the shopping list.

        Args:
            get_details: Fetch full product details for each item.
            query_filters: Optional Grocy API query filters.
        """
        raw = self._api.get_shopping_list(query_filters)
        shopping_list = [
            ShoppingListProduct.from_shopping_list_item(item) for item in raw
        ]
        if get_details:
            for item in shopping_list:
                item.get_details(self._api)
        return shopping_list

    def add_product(
        self,
        product_id: int,
        shopping_list_id: int | None = None,
        amount: float | None = None,
        quantity_unit_id: int | None = None,
    ):
        """Add a product to a shopping list.

        Args:
            product_id: The Grocy product ID.
            shopping_list_id: Target shopping list. Defaults to the first list.
            amount: Quantity to add.
            quantity_unit_id: Override the default quantity unit.
        """
        return self._api.add_product_to_shopping_list(
            product_id, shopping_list_id, amount, quantity_unit_id
        )

    def remove_product(
        self, product_id: int, shopping_list_id: int = 1, amount: float = 1
    ):
        """Remove a product from a shopping list.

        Args:
            product_id: The Grocy product ID.
            shopping_list_id: Target shopping list.
            amount: Quantity to remove.
        """
        return self._api.remove_product_in_shopping_list(
            product_id, shopping_list_id, amount
        )

    def mark_item_done(self, shopping_list_item_id: int, done: bool = True):
        """Mark a shopping list item as done or not done.

        Args:
            shopping_list_item_id: The shopping list item ID.
            done: Whether to mark as done (True) or not done (False).
        """
        return self._api.mark_shopping_list_item(shopping_list_item_id, done)

    def clear(self, shopping_list_id: int = 1):
        """Remove all items from a shopping list.

        Args:
            shopping_list_id: The shopping list ID.
        """
        return self._api.clear_shopping_list(shopping_list_id)

    def add_missing_products(self, shopping_list_id: int = 1):
        """Add all missing products to the shopping list.

        Args:
            shopping_list_id: The shopping list ID.
        """
        return self._api.add_missing_product_to_shopping_list(shopping_list_id)

    def add_overdue_products(self, shopping_list_id: int = 1):
        """Add all overdue products to the shopping list.

        Args:
            shopping_list_id: The shopping list ID.
        """
        return self._api.add_overdue_products_to_shopping_list(shopping_list_id)

    def add_expired_products(self, shopping_list_id: int = 1):
        """Add all expired products to the shopping list.

        Args:
            shopping_list_id: The shopping list ID.
        """
        return self._api.add_expired_products_to_shopping_list(shopping_list_id)
