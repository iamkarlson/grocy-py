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
