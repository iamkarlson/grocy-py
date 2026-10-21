import base64
import logging
from datetime import date, datetime

import pytest
import responses

from grocy.errors import GrocyError
from grocy.grocy import Grocy
from grocy.grocy_api_client import (
    DEFAULT_TIMEOUT,
    CurrentVolatileStockResponse,
    GrocyApiClient,
    StockLogResponse,
    TransactionType,
)


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


class TestRequests:
    BASE = "http://grocy.de:9192/api"

    @pytest.fixture
    def client(self):
        return GrocyApiClient(api_key="key", base_url="http://grocy.de")

    @responses.activate
    def test_every_request_has_the_default_timeout(self, client):
        responses.get(f"{self.BASE}/stock", json=[])

        client.get_stock()

        assert responses.calls[0].request.req_kwargs["timeout"] == DEFAULT_TIMEOUT

    @responses.activate
    def test_grocy_passes_its_timeout_to_the_client(self):
        responses.get(f"{self.BASE}/stock", json=[])

        Grocy("http://grocy.de", "key", timeout=5).stock.current()

        assert responses.calls[0].request.req_kwargs["timeout"] == 5

    @responses.activate
    def test_debug_level_of_the_application_reaches_the_client(self, client, caplog):
        responses.get(f"{self.BASE}/stock", json=[])
        caplog.set_level(logging.DEBUG, logger="grocy")

        client.get_stock()

        assert "GET /stock" in caplog.text

    @responses.activate
    @pytest.mark.parametrize("method", ["GET", "POST", "PUT", "DELETE"])
    def test_html_with_status_200_raises_grocy_error(self, client, method):
        html = "<html><body>Sign in</body></html>"
        responses.add(method, f"{self.BASE}/objects/products/1", body=html)
        send = {
            "GET": lambda: client._do_get_request("objects/products/1"),
            "POST": lambda: client._do_post_request("objects/products/1", {}),
            "PUT": lambda: client._do_put_request("objects/products/1", {}),
            "DELETE": lambda: client._do_delete_request("objects/products/1"),
        }[method]

        with pytest.raises(GrocyError) as error:
            send()

        assert error.value.status_code == 200
        assert error.value.message == html

    @responses.activate
    @pytest.mark.parametrize("method", ["GET", "POST", "PUT", "DELETE"])
    def test_empty_html_page_raises_grocy_error(self, client, method):
        # Grocy 4.7.1 answers an unknown API route like this.
        responses.add(
            method,
            f"{self.BASE}/nonexistent",
            body="",
            content_type="text/html; charset=UTF-8",
        )
        send = {
            "GET": lambda: client._do_get_request("nonexistent"),
            "POST": lambda: client._do_post_request("nonexistent", {}),
            "PUT": lambda: client._do_put_request("nonexistent", {}),
            "DELETE": lambda: client._do_delete_request("nonexistent"),
        }[method]

        with pytest.raises(GrocyError, match="no API route") as error:
            send()

        assert error.value.status_code == 200

    @responses.activate
    def test_upload_to_an_unroutable_file_name_raises_grocy_error(self, client):
        # The base64 form of this name contains "/", so Grocy matches no route.
        name = "проверка-ü 1.txt"
        url = f"{self.BASE}/{client._file_url('productpictures', name)}"
        responses.put(url, body="", content_type="text/html; charset=UTF-8")

        with pytest.raises(GrocyError, match="no API route"):
            client.upload_file("productpictures", name, b"data")

    @responses.activate
    @pytest.mark.parametrize(
        ("status", "content_type"),
        [(204, "application/json"), (200, "application/json"), (200, "text/plain")],
    )
    def test_empty_body_that_is_not_html_returns_none(
        self, client, status, content_type
    ):
        responses.delete(
            f"{self.BASE}/objects/tasks/1",
            body="",
            status=status,
            content_type=content_type,
        )

        assert client._do_delete_request("objects/tasks/1") is None

    @responses.activate
    def test_download_file_returns_the_bytes(self, client):
        name = base64.b64encode("Bäckerei.jpg".encode()).decode()
        responses.get(f"{self.BASE}/files/productpictures/{name}", body=b"\xff\xd8")

        assert client.download_file("productpictures", "Bäckerei.jpg") == b"\xff\xd8"
        assert responses.calls[0].request.headers["accept"] == "*/*"


class TestStockLogTransactionType:
    @staticmethod
    def _log(transaction_type: str) -> StockLogResponse:
        return StockLogResponse(
            id=1,
            product_id=1,
            amount=1,
            best_before_date="2026-10-20",
            purchased_date="2026-10-20",
            stock_id="s1",
            transaction_id="t1",
            transaction_type=transaction_type,
        )

    @pytest.mark.parametrize(
        "value",
        [
            "purchase",
            "consume",
            "inventory-correction",
            "product-opened",
            "transfer_from",
            "transfer_to",
            "stock-edit-old",
            "stock-edit-new",
            "self-production",
        ],
    )
    def test_every_grocy_type_is_an_enum_member(self, value):
        assert self._log(value).transaction_type is TransactionType(value)

    def test_unknown_type_is_kept_as_string(self):
        assert self._log("future-type").transaction_type == "future-type"
