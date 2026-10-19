from datetime import datetime

import pytest

from grocy.data_models.chore import AssignmentType, Chore, PeriodType
from grocy.data_models.user import User
from grocy.errors import GrocyError
from grocy.grocy_api_client import ChoreDetailsResponse


class TestChores:
    @pytest.mark.vcr
    def test_get_chores_valid(self, grocy):
        chores = grocy.chores.list(get_details=True)

        assert isinstance(chores, list)
        assert len(chores) == 6
        for chore in chores:
            assert isinstance(chore, Chore)
            assert isinstance(chore.id, int)
            assert isinstance(chore.last_tracked_time, datetime)
            assert isinstance(chore.next_estimated_execution_time, datetime)
            assert isinstance(chore.name, str)
            assert isinstance(chore.last_done_by, User)
            assert chore.userfields is not None
            assert isinstance(chore.userfields, (list, dict))

        chore = next(chore for chore in chores if chore.id == 6)
        assert chore.name == "Change the bed sheets"
        assert chore.period_config == "monday"

    @pytest.mark.vcr
    def test_get_chore_details(self, grocy):
        chore_details = grocy.chores.get(3)
        assert isinstance(chore_details, Chore)

        assert chore_details.name == "Take out the trash"
        assert chore_details.assignment_type == AssignmentType.RANDOM
        assert chore_details.last_done_by.id == 3
        assert chore_details.period_type == PeriodType.HOURLY
        assert chore_details.period_days is None
        assert chore_details.period_config is None
        assert chore_details.track_date_only is True
        assert chore_details.rollover is False
        assert chore_details.assignment_config == "1,2,3,4"
        assert chore_details.next_execution_assigned_user.id == 2
        assert chore_details.next_execution_assigned_to_user_id == 2
        assert chore_details.userfields is None

        assert chore_details.period_interval == 48
        assert chore_details.start_date == datetime(2025, 1, 1)
        assert chore_details.consume_product_on_execution is False
        assert chore_details.product_id is None
        assert chore_details.track_count == 19

    @pytest.mark.vcr
    def test_execute_chore_valid(self, grocy):
        result = grocy.chores.execute(1)
        assert result["chore_id"] == 1

    @pytest.mark.vcr
    def test_execute_chore_valid_with_data(self, grocy):
        result = grocy.chores.execute(
            1, done_by=1, tracked_time=datetime.now(), skipped=False
        )
        assert result["chore_id"] == 1
        assert result["done_by_user_id"] == 1

    @pytest.mark.vcr
    def test_execute_chore_invalid(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.chores.execute(1000)

        error = exc_info.value
        assert error.status_code == 400

    @pytest.mark.vcr
    def test_get_chores_filters_valid(self, grocy):
        query_filter = ["next_execution_assigned_to_user_id=1"]
        chores = grocy.chores.list(get_details=True, query_filters=query_filter)

        assert chores
        for item in chores:
            assert item.next_execution_assigned_to_user_id == 1

    @pytest.mark.vcr
    def test_get_chores_filters_invalid(self, grocy, invalid_query_filter):
        with pytest.raises(GrocyError) as exc_info:
            grocy.chores.list(get_details=True, query_filters=invalid_query_filter)

        error = exc_info.value
        assert error.status_code == 500


class TestChoreEnums:
    @staticmethod
    def _chore(**fields) -> Chore:
        data = {
            "id": 9,
            "name": "Chore",
            "period_type": "daily",
            "track_date_only": False,
            "rollover": False,
        }
        return Chore.from_details_response(ChoreDetailsResponse(chore=data | fields))

    def test_known_values_are_enum_members(self):
        chore = self._chore(assignment_type="random")

        assert chore.period_type is PeriodType.DAILY
        assert chore.assignment_type is AssignmentType.RANDOM

    def test_unknown_values_are_kept_as_strings(self, caplog):
        chore = self._chore(period_type="biweekly", assignment_type="round-robin")

        assert chore.period_type == "biweekly"
        assert chore.assignment_type == "round-robin"
        assert "Chore 9 has unknown period_type 'biweekly'" in caplog.text
        assert "Chore 9 has unknown assignment_type 'round-robin'" in caplog.text
