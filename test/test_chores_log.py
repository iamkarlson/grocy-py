from datetime import datetime
from unittest.mock import MagicMock

import pytest

from grocy.data_models.chore import Chore
from grocy.data_models.chore_log import ChoreLog
from grocy.data_models.user import User
from grocy.errors import GrocyError


class TestChoresLog:
    @pytest.mark.vcr
    def test_get_chores_log_valid(self, grocy):
        chores_log = grocy.chores_log.list(get_details=True)

        assert isinstance(chores_log, list)
        assert len(chores_log) == 152
        for chore_log in chores_log:
            assert isinstance(chore_log, ChoreLog)
            assert isinstance(chore_log.id, int)
            assert isinstance(chore_log.chore_id, int)
            assert isinstance(chore_log.tracked_time, datetime)
            assert isinstance(chore_log.done_by, int)
            assert isinstance(chore_log.row_created_timestamp, datetime)
            assert isinstance(chore_log.undone, bool)
            assert isinstance(chore_log.undone_timestamp, (datetime, type(None)))
            assert isinstance(chore_log.skipped, bool)
            assert isinstance(
                chore_log.scheduled_execution_time, (datetime, type(None))
            )
            assert isinstance(chore_log.chore, Chore)
            assert isinstance(chore_log.done_by_user, User)

        chore_log = next(chore_log for chore_log in chores_log if chore_log.id == 6)
        assert chore_log.chore_id == 6
        assert chore_log.done_by == 4
        assert chore_log.done_by_user.id == 4

    @pytest.mark.vcr
    def test_get_chore_log_details(self, grocy):
        chore_log_details = grocy.chores_log.get(3, get_details=True)
        assert isinstance(chore_log_details, ChoreLog)
        assert chore_log_details.id == 3

        assert chore_log_details.chore_id == 3
        assert chore_log_details.chore.id == 3

        assert chore_log_details.done_by == 4
        assert chore_log_details.done_by_user.id == 4

        assert chore_log_details.undone == 0
        assert chore_log_details.undone_timestamp is None
        assert chore_log_details.skipped == 0

    @pytest.mark.vcr
    def test_get_chores_log_filters_valid(self, grocy):
        query_filter = ["undone=1"]
        chores_log = grocy.chores_log.list(get_details=True, query_filters=query_filter)

        for item in chores_log:
            assert item.undone == 1

    @pytest.mark.vcr
    def test_get_chores_log_filters_invalid(self, grocy, invalid_query_filter):
        with pytest.raises(GrocyError) as exc_info:
            grocy.chores_log.list(get_details=True, query_filters=invalid_query_filter)

        error = exc_info.value
        assert error.status_code == 500

    def test_details_with_deleted_user_and_chore_keep_the_entry(self):
        api = MagicMock()
        api.get_userfields.return_value = {}
        api.get_chore.return_value = None
        api.get_user.return_value = None
        chore_log = ChoreLog(
            id=1,
            chore_id=1,
            tracked_time=datetime(2026, 10, 21),
            done_by=99,
            row_created_timestamp=datetime(2026, 10, 21),
            undone=False,
            skipped=False,
        )

        chore_log.get_details(api)

        assert chore_log.chore is None
        assert chore_log.done_by_user is None
