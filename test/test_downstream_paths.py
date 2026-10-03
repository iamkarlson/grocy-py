"""Manager methods that the Home Assistant integration calls but no cassette covers."""

from unittest.mock import MagicMock


def test_users_get_setting_delegates(grocy, mocker):
    get = mocker.patch.object(
        grocy.users._api, "get_user_setting", return_value={"value": 5}
    )

    assert grocy.users.get_setting("stock_due_soon_days") == {"value": 5}
    get.assert_called_once_with("stock_due_soon_days")


def test_recipes_all_fulfillment_delegates(grocy, mocker):
    rows = [MagicMock()]
    mocker.patch.object(
        grocy.recipes._api, "get_all_recipes_fulfillment", return_value=rows
    )

    assert grocy.recipes.all_fulfillment() is rows


def test_system_config_returns_none_for_empty_response(grocy, mocker):
    mocker.patch.object(grocy.system._api, "get_system_config", return_value=None)

    assert grocy.system.config() is None
