from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from ..data_models.system import SystemConfig, SystemInfo, SystemTime

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class SystemManager:
    """Access Grocy system information and configuration.

    Access via ``grocy.system``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def info(self) -> SystemInfo | None:
        """Get Grocy system version and environment info."""
        raw = self._api.get_system_info()
        if raw:
            return SystemInfo.from_dto(raw)
        return None

    def time(self) -> SystemTime | None:
        """Get the server's current time and timezone."""
        raw = self._api.get_system_time()
        if raw:
            return SystemTime.from_dto(raw)
        return None

    def config(self) -> SystemConfig | None:
        """Get the Grocy system configuration."""
        raw = self._api.get_system_config()
        if raw:
            return SystemConfig.from_dto(raw)
        return None

    def db_changed_time(self) -> datetime | None:
        """Get the timestamp of the last database change."""
        return self._api.get_last_db_changed()
