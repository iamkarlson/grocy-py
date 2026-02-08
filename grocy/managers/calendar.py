from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class CalendarManager:
    """Access Grocy calendar data in iCal format.

    Access via ``grocy.calendar``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def ical(self) -> str | None:
        """Get the calendar as an iCal string."""
        return self._api.get_calendar_ical()

    def sharing_link(self) -> str | None:
        """Get the calendar sharing URL."""
        return self._api.get_calendar_sharing_link()
