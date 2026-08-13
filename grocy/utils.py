import zoneinfo
from datetime import datetime

from tzlocal import get_localzone


def parse_date(input_value):
    """Parse an ISO 8601 date string into a datetime, returning None for empty input."""
    if input_value == "" or input_value is None:
        return None
    return datetime.fromisoformat(input_value)


def parse_int(input_value, default_value=None):
    """Parse a value as an integer, returning a default if conversion fails."""
    if input_value is None:
        return default_value
    try:
        return int(input_value)
    except ValueError:
        return default_value


def parse_float(input_value, default_value=None):
    """Parse a value as a float, returning a default if conversion fails."""
    if input_value is None:
        return default_value
    try:
        return float(input_value)
    except ValueError:
        return default_value


def parse_bool_int(input_value):
    """Parse a value as a boolean integer (0/1), returning False on failure."""
    if input_value is None:
        return False
    try:
        num = int(input_value)
        return bool(num)
    except ValueError:
        return False


def localize_datetime(timestamp: datetime) -> datetime:
    """Attach the local timezone to a naive datetime.

    If the datetime already has timezone info, it is returned unchanged.
    """
    if timestamp.tzinfo is not None:
        return timestamp

    local_zone = _detect_local_zone()
    if local_zone is not None:
        # Treat naive input as already in local time so we just attach tzinfo.
        return timestamp.replace(tzinfo=local_zone)

    return timestamp.astimezone()


def grocy_datetime_str(timestamp: datetime) -> str:
    """Format a datetime as a Grocy-compatible string (``YYYY-MM-DD HH:MM:SS``)."""
    if timestamp is None:
        return ""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def _detect_local_zone():
    local_zone = get_localzone()
    if isinstance(local_zone, str):
        return zoneinfo.ZoneInfo(local_zone)
    return local_zone
