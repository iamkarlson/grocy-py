from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from ..data_models.generic import EntityType
from ..data_models.product import Group, Product
from ..grocy_api_client import ProductData, TransactionType

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class StockManager:
    """Manage product stock levels, entries, and transactions.

    Access via `grocy.stock`.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def current(self) -> list[Product]:
        """Get all products currently in stock."""
        raw_stock = self._api.get_stock()
        return [Product.from_stock_response(resp) for resp in raw_stock]

    def due_products(self, get_details: bool = False) -> list[Product]:
        """Get products that are due soon.

        Args:
            get_details: Fetch full product details for each item.
        """
        raw = self._api.get_volatile_stock().due_products
        products = [Product.from_stock_response(resp) for resp in raw] if raw else []
        if get_details:
            for item in products:
                item.get_details(self._api)
        return products

    def overdue_products(self, get_details: bool = False) -> list[Product]:
        """Get products that are past their best-before date.

        Args:
            get_details: Fetch full product details for each item.
        """
        raw = self._api.get_volatile_stock().overdue_products
        products = [Product.from_stock_response(resp) for resp in raw] if raw else []
        if get_details:
            for item in products:
                item.get_details(self._api)
        return products

    def expired_products(self, get_details: bool = False) -> list[Product]:
        """Get products that have expired.

        Args:
            get_details: Fetch full product details for each item.
        """
        raw = self._api.get_volatile_stock().expired_products
        products = [Product.from_stock_response(resp) for resp in raw] if raw else []
        if get_details:
            for item in products:
                item.get_details(self._api)
        return products

    def missing_products(self, get_details: bool = False) -> list[Product]:
        """Get products that are below their minimum stock amount.

        Args:
            get_details: Fetch full product details for each item.
        """
        raw = self._api.get_volatile_stock().missing_products
        products = [Product.from_missing_response(resp) for resp in raw] if raw else []
        if get_details:
            for item in products:
                item.get_details(self._api)
        return products

    def product(self, product_id: int) -> Product | None:
        """Get a single product by ID."""
        resp = self._api.get_product(product_id)
        if resp:
            return Product.from_details_response(resp)
        return None

    def product_by_barcode(self, barcode: str) -> Product | None:
        """Get a single product by barcode."""
        resp = self._api.get_product_by_barcode(barcode)
        if resp:
            return Product.from_details_response(resp)
        return None

    def all_products(self) -> list[Product]:
        """Get all products regardless of stock status."""
        raw_products = self._api.get_generic_objects_for_type(EntityType.PRODUCTS)
        if not raw_products:
            return []
        product_datas = [ProductData(**product) for product in raw_products]
        return [Product.from_product_data(product) for product in product_datas]

    def add(
        self,
        product_id: int,
        amount: float,
        price: float,
        best_before_date: datetime | None = None,
        transaction_type: TransactionType = TransactionType.PURCHASE,
    ):
        """Add stock for a product.

        Args:
            product_id: The Grocy product ID.
            amount: Quantity to add.
            price: Unit price.
            best_before_date: Expiry date. Defaults to the product's configured default.
            transaction_type: Type of stock transaction.
        """
        return self._api.add_product(
            product_id, amount, price, best_before_date, transaction_type
        )

    def consume(
        self,
        product_id: int,
        amount: float = 1,
        spoiled: bool = False,
        transaction_type: TransactionType = TransactionType.CONSUME,
        allow_subproduct_substitution: bool = False,
    ):
        """Consume stock for a product.

        Args:
            product_id: The Grocy product ID.
            amount: Quantity to consume.
            spoiled: Whether the consumed amount was spoiled.
            transaction_type: Type of stock transaction.
            allow_subproduct_substitution: Allow consuming from sub-products.
        """
        return self._api.consume_product(
            product_id, amount, spoiled, transaction_type, allow_subproduct_substitution
        )

    def open(
        self,
        product_id: int,
        amount: float = 1,
        allow_subproduct_substitution: bool = False,
    ):
        """Mark stock of a product as opened.

        Args:
            product_id: The Grocy product ID.
            amount: Quantity to mark as opened.
            allow_subproduct_substitution: Allow opening from sub-products.
        """
        return self._api.open_product(product_id, amount, allow_subproduct_substitution)

    def transfer(
        self,
        product_id: int,
        amount: float,
        location_from: int,
        location_to: int,
    ):
        """Transfer stock of a product between locations.

        Args:
            product_id: The Grocy product ID.
            amount: Quantity to transfer.
            location_from: Source location ID.
            location_to: Destination location ID.
        """
        return self._api.transfer_product(
            product_id, amount, location_from, location_to
        )

    def inventory(
        self,
        product_id: int,
        new_amount: float,
        best_before_date: datetime | None = None,
        shopping_location_id: int | None = None,
        location_id: int | None = None,
        price: float | None = None,
        get_details: bool = True,
    ) -> Product | None:
        """Perform a stock inventory correction for a product.

        Args:
            product_id: The Grocy product ID.
            new_amount: The corrected total amount.
            best_before_date: Expiry date for the corrected stock.
            shopping_location_id: Where the product was purchased.
            location_id: Storage location ID.
            price: Unit price.
            get_details: Fetch full product details after correction.
        """
        resp = self._api.inventory_product(
            product_id,
            new_amount,
            best_before_date,
            shopping_location_id,
            location_id,
            price,
        )
        if resp:
            product = Product.from_stock_log_response(resp)
            if get_details:
                product.get_details(self._api)
            return product
        return None

    def add_by_barcode(
        self,
        barcode: str,
        amount: float,
        price: float,
        best_before_date: datetime | None = None,
        get_details: bool = True,
    ) -> Product | None:
        """Add stock for a product identified by barcode.

        Args:
            barcode: Product barcode.
            amount: Quantity to add.
            price: Unit price.
            best_before_date: Expiry date.
            get_details: Fetch full product details after adding.
        """
        resp = self._api.add_product_by_barcode(
            barcode, amount, price, best_before_date
        )
        if resp:
            product = Product.from_stock_log_response(resp)
            if get_details:
                product.get_details(self._api)
            return product
        return None

    def consume_by_barcode(
        self,
        barcode: str,
        amount: float = 1,
        spoiled: bool = False,
        get_details: bool = True,
    ) -> Product | None:
        """Consume stock for a product identified by barcode.

        Args:
            barcode: Product barcode.
            amount: Quantity to consume.
            spoiled: Whether the consumed amount was spoiled.
            get_details: Fetch full product details after consuming.
        """
        resp = self._api.consume_product_by_barcode(barcode, amount, spoiled)
        if resp:
            product = Product.from_stock_log_response(resp)
            if get_details:
                product.get_details(self._api)
            return product
        return None

    def transfer_by_barcode(
        self,
        barcode: str,
        amount: float,
        location_from: int,
        location_to: int,
    ):
        """Transfer stock of a product identified by barcode.

        Args:
            barcode: Product barcode.
            amount: Quantity to transfer.
            location_from: Source location ID.
            location_to: Destination location ID.
        """
        return self._api.transfer_product_by_barcode(
            barcode, amount, location_from, location_to
        )

    def open_by_barcode(self, barcode: str, amount: float = 1):
        """Mark stock of a product identified by barcode as opened."""
        return self._api.open_product_by_barcode(barcode, amount)

    def inventory_by_barcode(
        self,
        barcode: str,
        new_amount: float,
        best_before_date: datetime | None = None,
        location_id: int | None = None,
        price: float | None = None,
        get_details: bool = True,
    ) -> Product | None:
        """Perform a stock inventory correction by barcode.

        Args:
            barcode: Product barcode.
            new_amount: The corrected total amount.
            best_before_date: Expiry date for the corrected stock.
            location_id: Storage location ID.
            price: Unit price.
            get_details: Fetch full product details after correction.
        """
        resp = self._api.inventory_product_by_barcode(
            barcode, new_amount, best_before_date, location_id, price
        )
        if resp:
            product = Product.from_stock_log_response(resp)
            if get_details:
                product.get_details(self._api)
            return product
        return None

    def merge(self, product_id_keep: int, product_id_remove: int):
        """Merge two products, keeping one and removing the other.

        Args:
            product_id_keep: ID of the product to keep.
            product_id_remove: ID of the product to remove.
        """
        return self._api.merge_products(product_id_keep, product_id_remove)

    def entry(self, entry_id: int):
        """Get a single stock entry by ID."""
        return self._api.get_stock_entry(entry_id)

    def edit_entry(self, entry_id: int, data: dict):
        """Edit a stock entry.

        Args:
            entry_id: The stock entry ID.
            data: Fields to update.
        """
        return self._api.edit_stock_entry(entry_id, data)

    def product_entries(self, product_id: int):
        """Get all stock entries for a product."""
        return self._api.get_product_stock_entries(product_id)

    def product_locations(self, product_id: int):
        """Get stock locations for a product."""
        return self._api.get_product_stock_locations(product_id)

    def product_price_history(self, product_id: int):
        """Get price history for a product."""
        return self._api.get_product_price_history(product_id)

    def entries_by_location(self, location_id: int):
        """Get all stock entries at a given location."""
        return self._api.get_stock_entries_by_location(location_id)

    def booking(self, booking_id: int):
        """Get a stock booking by ID."""
        return self._api.get_stock_booking(booking_id)

    def undo_booking(self, booking_id: int):
        """Undo a stock booking."""
        return self._api.undo_stock_booking(booking_id)

    def transaction(self, transaction_id: str):
        """Get all log entries for a stock transaction."""
        return self._api.get_stock_transactions(transaction_id)

    def undo_transaction(self, transaction_id: str):
        """Undo a stock transaction."""
        return self._api.undo_stock_transaction(transaction_id)

    def barcode_lookup(self, barcode: str):
        """Look up a barcode using the external barcode lookup service."""
        return self._api.external_barcode_lookup(barcode)

    def product_groups(self, query_filters: list[str] | None = None) -> list[Group]:
        """Get all product groups."""
        raw_groups = self._api.get_product_groups(query_filters)
        return [
            Group(id=resp.id, name=resp.name, description=resp.description)
            for resp in raw_groups
        ]

    def upload_product_picture(self, product_id: int, pic_path: str):
        """Upload a picture for a product.

        Args:
            product_id: The Grocy product ID.
            pic_path: Local filesystem path to the image file.
        """
        self._api.upload_product_picture(product_id, pic_path)
        return self._api.update_product_pic(product_id)
