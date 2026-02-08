from datetime import datetime
import zoneinfo

from tzlocal import get_localzone


def parse_date(input_value):
    if input_value == "" or input_value is None:
        return None
    return datetime.fromisoformat(input_value)


def parse_int(input_value, default_value=None):
    if input_value is None:
        return default_value
    try:
        return int(input_value)
    except ValueError:
        return default_value


def parse_float(input_value, default_value=None):
    if input_value is None:
        return default_value
    try:
        return float(input_value)
    except ValueError:
        return default_value


def parse_bool_int(input_value):
    if input_value is None:
        return False
    try:
        num = int(input_value)
        return bool(num)
    except ValueError:
        return False


def localize_datetime(timestamp: datetime) -> datetime:
    if timestamp.tzinfo is not None:
        return timestamp

    local_zone = _detect_local_zone()
    if local_zone is not None:
        # Treat naive input as already in local time so we just attach tzinfo.
        return timestamp.replace(tzinfo=local_zone)

    return timestamp.astimezone()


def grocy_datetime_str(timestamp: datetime) -> str:
    if timestamp is None:
        return ""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def _detect_local_zone():
    local_zone = get_localzone()
    if isinstance(local_zone, str):
        return zoneinfo.ZoneInfo(local_zone)
    return local_zone
