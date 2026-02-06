from test.test_const import CONST_API_KEY, CONST_BASE_URL, CONST_PORT, CONST_SSL

import pytest

from pygrocy2.grocy import Grocy


@pytest.fixture
def grocy():
    return Grocy(CONST_BASE_URL, CONST_API_KEY, verify_ssl=CONST_SSL, port=CONST_PORT)


# noinspection PyProtectedMember
@pytest.fixture
def grocy_api_client(grocy):
    return grocy._api_client


@pytest.fixture(scope="module")
def vcr_config():
    return {"record_mode": "once", "decode_compressed_response": True}


@pytest.fixture
def invalid_query_filter() -> list[str]:
    return ["invalid"]
