import pytest

from grocy.data_models.product import Product
from grocy.errors import GrocyError
from grocy.grocy_api_client import CurrentVolatileStockResponse


class TestStock:
    @pytest.mark.vcr
    def test_get_stock_valid(self, grocy):
        stock = grocy.stock.current()

        assert isinstance(stock, list)
        assert len(stock) == 24
        for prod in stock:
            assert isinstance(prod, Product)

    @pytest.mark.vcr
    def test_get_due_products_valid(self, grocy):
        due_products = grocy.stock.due_products(True)

        assert isinstance(due_products, list)
        assert len(due_products) == 4
        for prod in due_products:
            assert isinstance(prod, Product)

    @pytest.mark.vcr
    def test_get_expired_products_valid(self, grocy):
        expired_products = grocy.stock.expired_products(True)

        assert isinstance(expired_products, list)
        assert len(expired_products) == 1
        for prod in expired_products:
            assert isinstance(prod, Product)

    @pytest.mark.vcr
    def test_get_missing_products_valid(self, grocy):
        missing_products = grocy.stock.missing_products(True)

        assert isinstance(missing_products, list)
        assert len(missing_products) == 1
        for prod in missing_products:
            assert isinstance(prod, Product)
            assert isinstance(prod.amount_missing, float)
            assert isinstance(prod.is_partly_in_stock, bool)

        product = next(product for product in missing_products if product.id == 3)
        assert product.is_partly_in_stock is True
        assert product.amount_missing == 4.0

    @pytest.mark.vcr
    def test_get_overdue_products_valid(self, grocy):
        overdue_products = grocy.stock.overdue_products(True)

        assert isinstance(overdue_products, list)
        assert len(overdue_products) == 4
        for prod in overdue_products:
            assert isinstance(prod, Product)

    @pytest.mark.vcr
    def test_open_product_valid(self, grocy):
        grocy.stock.open(13, 1)

    @pytest.mark.vcr
    def test_open_product_error(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.stock.open(13, 0)

        error = exc_info.value
        assert error.status_code == 400


class TestStockVolatile:
    """`due_soon_days` plumbing, from StockManager down to the API client.

    Grocy defaults the due-soon window to 5 days and ignores the
    stock_due_soon_days system setting unless the query param is sent, so
    callers that read that setting need to be able to pass it through.
    """

    @pytest.fixture
    def get_volatile_stock(self, grocy, mocker):
        return mocker.patch.object(
            grocy._api_client,
            "get_volatile_stock",
            return_value=CurrentVolatileStockResponse(),
        )

    def test_volatile_defaults_to_none(self, grocy, get_volatile_stock):
        grocy.stock.volatile()

        get_volatile_stock.assert_called_once_with(None)

    def test_volatile_forwards_due_soon_days(self, grocy, get_volatile_stock):
        grocy.stock.volatile(10)

        get_volatile_stock.assert_called_once_with(10)

    def test_volatile_returns_raw_response(self, grocy, get_volatile_stock):
        result = grocy.stock.volatile()

        assert result is get_volatile_stock.return_value

    def test_due_products_defaults_to_none(self, grocy, get_volatile_stock):
        grocy.stock.due_products()

        get_volatile_stock.assert_called_once_with(None)

    def test_due_products_forwards_due_soon_days(self, grocy, get_volatile_stock):
        grocy.stock.due_products(get_details=False, due_soon_days=10)

        get_volatile_stock.assert_called_once_with(10)

    def test_due_products_handles_empty_response(self, grocy, get_volatile_stock):
        assert grocy.stock.due_products(due_soon_days=10) == []

    @pytest.mark.vcr
    def test_due_products_with_due_soon_days_hits_grocy(self, grocy):
        """Round-trip against a real Grocy to prove the query param is accepted."""
        due_products = grocy.stock.due_products(True, due_soon_days=90)

        assert isinstance(due_products, list)
        for prod in due_products:
            assert isinstance(prod, Product)
