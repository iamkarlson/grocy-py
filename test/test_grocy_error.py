import requests

from grocy.errors import GrocyError


def make_response(status: int, body: bytes) -> requests.Response:
    response = requests.Response()
    response.status_code = status
    response._content = body
    response.encoding = "utf-8"
    return response


def test_html_error_page_becomes_grocy_error_with_status_and_snippet():
    html = b"<html><body><h1>502 Bad Gateway</h1></body></html>"

    error = GrocyError(make_response(502, html))

    assert isinstance(error, GrocyError)
    assert error.status_code == 502
    assert error.message == html.decode()


def test_json_without_error_message_has_no_message():
    error = GrocyError(make_response(500, b'{"foo": 1}'))

    assert error.status_code == 500
    assert error.message is None


def test_json_error_message_is_used():
    error = GrocyError(make_response(400, b'{"error_message": "bad input"}'))

    assert error.status_code == 400
    assert error.message == "bad input"


def test_empty_body_has_no_message():
    error = GrocyError(make_response(404, b""))

    assert error.status_code == 404
    assert error.message is None


def test_str_shows_status_and_message():
    error = GrocyError(make_response(400, b'{"error_message": "bad input"}'))

    assert str(error) == "HTTP 400: bad input"


def test_str_without_message_shows_status():
    assert str(GrocyError(make_response(404, b""))) == "HTTP 404"
