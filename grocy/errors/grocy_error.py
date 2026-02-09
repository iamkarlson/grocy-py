from requests import Response


class GrocyError(Exception):
    """Exception raised when the Grocy API returns an error response.

    Attributes:
        status_code: HTTP status code from the response.
        message: Error message from the API, if available.
    """

    def __init__(self, response: Response):
        self._status_code = response.status_code

        if len(response.text) > 0:
            json = response.json()
            self._message = json["error_message"]
        else:
            self._message = None

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
