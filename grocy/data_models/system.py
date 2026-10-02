from datetime import date, datetime

from pydantic import BaseModel


class SystemInfo(BaseModel):
    """Grocy server version and environment information."""

    grocy_version: str
    grocy_release_date: date
    php_version: str
    sqlite_version: str
    os: str
    client: str

    @classmethod
    def from_dto(cls, dto) -> "SystemInfo":
        """Create from a system info API response."""
        return cls(
            grocy_version=dto.grocy_version_info.version,
            grocy_release_date=dto.grocy_version_info.release_date,
            php_version=dto.php_version,
            sqlite_version=dto.sqlite_version,
            os=dto.os,
            client=dto.client,
        )


class SystemTime(BaseModel):
    """Server time and timezone information."""

    timezone: str
    time_local: datetime
    time_local_sqlite3: datetime
    time_utc: datetime
    timestamp: int

    @classmethod
    def from_dto(cls, dto) -> "SystemTime":
        """Create from a system time API response."""
        return cls(
            timezone=dto.timezone,
            time_local=dto.time_local,
            time_local_sqlite3=dto.time_local_sqlite3,
            time_utc=dto.time_utc,
            timestamp=dto.timestamp,
        )


class SystemConfig(BaseModel):
    """Grocy system configuration including locale, currency, and feature flags."""

    username: str | None = None
    base_path: str
    base_url: str
    mode: str
    default_locale: str
    locale: str
    currency: str
    enabled_features: list[str] = []

    @classmethod
    def from_dto(cls, dto) -> "SystemConfig":
        """Create from a system config API response."""
        enabled_features = [
            feature
            for feature, value in dto.feature_flags.items()
            if value not in (False, "0")
        ]
        return cls(
            username=dto.username,
            base_path=dto.base_path,
            base_url=dto.base_url,
            mode=dto.mode,
            default_locale=dto.default_locale,
            locale=dto.locale,
            currency=dto.currency,
            enabled_features=enabled_features,
        )
