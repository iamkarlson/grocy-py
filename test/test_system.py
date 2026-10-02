from datetime import date, datetime
from typing import Any, ClassVar

import pytest

from grocy.data_models.system import SystemConfig, SystemInfo, SystemTime
from grocy.grocy_api_client import SystemConfigDto


class TestSystem:
    @pytest.mark.vcr
    def test_get_last_db_changed_valid(self, grocy):
        timestamp = grocy.system.db_changed_time()

        assert isinstance(timestamp, datetime)
        assert timestamp.year == 2026
        assert timestamp.month == 1
        assert timestamp.day == 7

    @pytest.mark.vcr
    def test_get_system_info_valid(self, grocy):
        system_info = grocy.system.info()

        assert isinstance(system_info, SystemInfo)
        assert isinstance(system_info.grocy_release_date, date)
        assert system_info.grocy_version == "4.5.0"
        assert system_info.php_version == "8.3.19"
        assert system_info.sqlite_version == "3.48.0"

    @pytest.mark.vcr
    def test_get_system_time_valid(self, grocy):
        system_time = grocy.system.time()

        assert isinstance(system_time, SystemTime)
        assert isinstance(system_time.time_local, datetime)
        assert isinstance(system_time.time_local_sqlite3, datetime)
        assert isinstance(system_time.time_utc, datetime)

        assert system_time.timezone == "UTC"
        assert system_time.timestamp == 1767826820

    @pytest.mark.vcr
    def test_get_system_config_valid(self, grocy):
        system_config = grocy.system.config()

        assert isinstance(system_config, SystemConfig)

        assert system_config.username == "Demo User"
        assert system_config.currency == "USD"
        assert system_config.locale == "en"
        assert "FEATURE_FLAG_TASKS" in system_config.enabled_features
        assert "FEATURE_FLAG_THERMAL_PRINTER" not in system_config.enabled_features


class TestSystemConfigUsername:
    """grocy 4.7.0 removed the user-scoped constants from GET /system/config."""

    PAYLOAD: ClassVar[dict[str, Any]] = {
        "BASE_PATH": "",
        "BASE_URL": "/",
        "MODE": "production",
        "DEFAULT_LOCALE": "en",
        "LOCALE": "en",
        "CURRENCY": "USD",
        "FEATURE_FLAG_TASKS": True,
        "FEATURE_FLAG_THERMAL_PRINTER": False,
    }

    def test_username_absent_is_none(self):
        dto = SystemConfigDto(**self.PAYLOAD)

        assert dto.username is None

    def test_username_present_is_kept(self):
        dto = SystemConfigDto(**self.PAYLOAD, USER_USERNAME="Demo User")

        assert dto.username == "Demo User"

    def test_from_dto_without_username(self):
        system_config = SystemConfig.from_dto(SystemConfigDto(**self.PAYLOAD))

        assert isinstance(system_config, SystemConfig)
        assert system_config.username is None
        assert system_config.currency == "USD"
        assert "FEATURE_FLAG_TASKS" in system_config.enabled_features
        assert "FEATURE_FLAG_THERMAL_PRINTER" not in system_config.enabled_features
