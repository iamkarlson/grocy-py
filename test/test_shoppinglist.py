import pytest

from grocy.data_models.product import Product, ShoppingListProduct
from grocy.errors import GrocyError


class TestShoppingList:
    @pytest.mark.vcr
    def test_get_shopping_list_valid(self, grocy):
        shopping_list = grocy.shopping_list.items(True)

        assert isinstance(shopping_list, list)
        assert len(shopping_list) == 5
        for item in shopping_list:
            assert isinstance(item, ShoppingListProduct)
            assert isinstance(item.id, int)
            assert isinstance(item.done, bool)
            if item.product_id:
                assert isinstance(item.product_id, int)
                assert isinstance(item.product, Product)
                assert isinstance(item.product.id, int)
            assert isinstance(item.amount, float)
            if item.note:
                assert isinstance(item.note, str)

        item = next(item for item in shopping_list if item.id == 2)
        assert item.note is None
        assert item.amount == 1.0
        assert item.product_id == 20

    @pytest.mark.vcr
    def test_add_missing_product_to_shopping_list_valid(self, grocy):
        assert grocy.shopping_list.add_missing_products() is None

    @pytest.mark.vcr
    def test_add_product_to_shopping_list_valid(self, grocy):
        grocy.shopping_list.add_product(19)

    @pytest.mark.vcr
    def test_add_nonexistant_product_to_shopping_list(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.shopping_list.add_product(3000)

        error = exc_info.value
        assert error.status_code == 400
        assert error.message == "Product does not exist or is inactive"

    @pytest.mark.vcr
    def test_add_missing_products_to_nonexistant_shopping_list(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.shopping_list.add_missing_products(3000)

        error = exc_info.value
        assert error.status_code == 400
        assert error.message == "Shopping list does not exist"

    @pytest.mark.vcr
    def test_clear_shopping_list_valid(self, grocy):
        grocy.shopping_list.clear()

    @pytest.mark.vcr
    def test_remove_product_in_shopping_list_valid(self, grocy):
        grocy.shopping_list.remove_product(20)

    @pytest.mark.vcr
    def test_get_shopping_list_filters_valid(self, grocy):
        query_filter = ["note~snacks"]
        shopping_list = grocy.shopping_list.items(
            get_details=True, query_filters=query_filter
        )

        for item in shopping_list:
            assert "snacks" in item.note

    @pytest.mark.vcr
    def test_get_shopping_list_filters_invalid(self, grocy, invalid_query_filter):
        with pytest.raises(GrocyError) as exc_info:
            grocy.shopping_list.items(
                get_details=True, query_filters=invalid_query_filter
            )

        error = exc_info.value
        assert error.status_code == 500

    @pytest.mark.vcr
    def test_mark_item_done(self, grocy):
        shopping_list = grocy.shopping_list.items()
        item = next(item for item in shopping_list if item.id == 2)

        # Mark as done
        grocy.shopping_list.mark_item_done(item.id, True)
        shopping_list = grocy.shopping_list.items()
        item_done = next(item for item in shopping_list if item.id == 2)
        assert item_done.done is True

        # Mark as not done
        grocy.shopping_list.mark_item_done(item.id, False)
        shopping_list = grocy.shopping_list.items()
        item_undone = next(item for item in shopping_list if item.id == 2)
        assert item_undone.done is False
