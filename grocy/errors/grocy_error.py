from requests import Response

_SNIPPET_LENGTH = 200


def _error_message(response: Response) -> str | None:
    """Return the API's error message, or a snippet of a body that is not Grocy JSON."""
    text = response.text
    if not text:
        return None
    try:
        body = response.json()
    except ValueError:
        return text[:_SNIPPET_LENGTH]
    if isinstance(body, dict):
        return body.get("error_message")
    return text[:_SNIPPET_LENGTH]


class GrocyError(Exception):
    """Exception raised when the Grocy API returns an error response.

    Attributes:
        status_code: HTTP status code from the response.
        message: Error message from the API, if available.
    """

    def __init__(self, response: Response, message: str | None = None):
        self._status_code = response.status_code
        self._message = message or _error_message(response)
        detail = f": {self._message}" if self._message else ""
        super().__init__(f"HTTP {self._status_code}{detail}")

    @property
    def status_code(self) -> int:
        """HTTP status code from the error response."""
        return self._status_code

    @property
    def message(self) -> str:
        """Error message from the API."""
        return self._message

    @property
    def is_client_error(self) -> bool:
        """True if this is a 4xx client error."""
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        """True if this is a 5xx server error."""
        return self.status_code >= 500
