from datetime import date, datetime

import pytest

from grocy.grocy_api_client import CurrentVolatileStockResponse, GrocyApiClient


class TestGrocyApiClient:
    def test_url_only(self):
        client = GrocyApiClient(api_key="", base_url="http://grocy.de")
        assert client._base_url == "http://grocy.de:9192/api/"

    def test_url_and_port(self):
        client = GrocyApiClient(api_key="", base_url="http://grocy.de", port=1234)
        assert client._base_url == "http://grocy.de:1234/api/"

    def test_url_and_port_and_path(self):
        client = GrocyApiClient(
            api_key="", base_url="http://grocy.de", port=1234, path="my/custom/path"
        )
        assert client._base_url == "http://grocy.de:1234/my/custom/path/api/"

    def test_url_and_path(self):
        client = GrocyApiClient(
            api_key="", base_url="http://grocy.de", path="my/custom/path"
        )
        assert client._base_url == "http://grocy.de:9192/my/custom/path/api/"


class TestGetVolatileStock:
    @pytest.fixture
    def client(self):
        return GrocyApiClient(api_key="", base_url="http://grocy.de")

    def test_omits_query_param_by_default(self, client, mocker):
        do_get = mocker.patch.object(client, "_do_get_request", return_value={})

        client.get_volatile_stock()

        do_get.assert_called_once_with("stock/volatile")

    def test_appends_due_soon_days(self, client, mocker):
        do_get = mocker.patch.object(client, "_do_get_request", return_value={})

        client.get_volatile_stock(10)

        do_get.assert_called_once_with("stock/volatile?due_soon_days=10")

    def test_appends_due_soon_days_of_zero(self, client, mocker):
        """Zero is a meaningful window, not an "unset" sentinel."""
        do_get = mocker.patch.object(client, "_do_get_request", return_value={})

        client.get_volatile_stock(0)

        do_get.assert_called_once_with("stock/volatile?due_soon_days=0")

    @pytest.mark.parametrize("payload", [None, {}, ""])
    def test_empty_payload_returns_empty_response(self, client, mocker, payload):
        mocker.patch.object(client, "_do_get_request", return_value=payload)

        result = client.get_volatile_stock()

        assert isinstance(result, CurrentVolatileStockResponse)
        assert result.due_products is None
        assert result.overdue_products is None
        assert result.expired_products is None
        assert result.missing_products is None


class TestBestBeforeDate:
    """A date-only ``best_before_date`` must work on every write path.

    Home Assistant's ``cv.date`` validator yields a ``datetime.date``, so all
    four Grocy write endpoints have to accept one, not just ``add_product``.
    """

    @pytest.fixture
    def client(self):
        return GrocyApiClient(api_key="", base_url="http://grocy.de")

    @pytest.fixture
    def do_post(self, client, mocker):
        return mocker.patch.object(client, "_do_post_request", return_value=None)

    @pytest.fixture(
        params=[
            "add_product",
            "inventory_product",
            "add_product_by_barcode",
            "inventory_product_by_barcode",
        ]
    )
    def call(self, request, client):
        """Return a callable invoking one write path with the given date."""
        name = request.param

        def invoke(best_before_date):
            if name == "add_product":
                return client.add_product(1, 2.0, 1.99, best_before_date)
            if name == "inventory_product":
                return client.inventory_product(1, 2.0, best_before_date)
            if name == "add_product_by_barcode":
                return client.add_product_by_barcode("123", 2.0, 1.99, best_before_date)
            return client.inventory_product_by_barcode("123", 2.0, best_before_date)

        return invoke

    def test_accepts_plain_date(self, call, do_post):
        call(date(2019, 1, 19))

        assert do_post.call_args[0][1]["best_before_date"] == "2019-01-19"

    def test_accepts_datetime(self, call, do_post):
        call(datetime(2019, 1, 19, 23, 45, 12))

        assert do_post.call_args[0][1]["best_before_date"] == "2019-01-19"

    def test_omitted_leaves_field_out(self, call, do_post):
        call(None)

        assert "best_before_date" not in do_post.call_args[0][1]
