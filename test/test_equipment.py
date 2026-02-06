from datetime import datetime

import pytest

from pygrocy2.data_models.equipment import Equipment
from pygrocy2.errors import GrocyError
from pygrocy2.grocy import Grocy
from pygrocy2.grocy_api_client import (
    EquipmentDetailsResponse,
    EquipmentData,
)


class TestEquipment:
    def test_init_from_equipment_data(self):
        """Test Equipment initialization from EquipmentData with minimal fields."""
        response = EquipmentData(
            id=1, name="Test Equipment", row_created_timestamp=datetime(2025, 3, 23)
        )
        equipment = Equipment(response)

        assert equipment.id == 1
        assert equipment.name == "Test Equipment"
        assert equipment.description is None
        assert equipment.instruction_manual_file_name is None
        assert equipment.created_timestamp == datetime(2025, 3, 23)
        assert equipment.userfields is None

    def test_init_from_details_response(self):
        """Test Equipment initialization from EquipmentDetailsResponse."""
        equipment_data = EquipmentData(
            id=1,
            name="Test Equipment",
            description="Test Description",
            instruction_manual_file_name="manual.pdf",
            row_created_timestamp=datetime(2025, 3, 23),
            userfields={"custom_field": "custom_value"},
        )

        response = EquipmentDetailsResponse(equipment=equipment_data)

        equipment = Equipment(response)

        assert equipment.id == 1
        assert equipment.name == "Test Equipment"
        assert equipment.description == "Test Description"
        assert equipment.instruction_manual_file_name == "manual.pdf"
        assert equipment.created_timestamp == datetime(2025, 3, 23)
        assert equipment.userfields == {"custom_field": "custom_value"}

    def test_as_dict(self):
        """Test Equipment.as_dict method."""
        equipment_data = EquipmentData(
            id=1,
            name="Test Equipment",
            description="Test Description",
            instruction_manual_file_name="manual.pdf",
            row_created_timestamp=datetime(2025, 3, 23),
            userfields={"custom_field": "custom_value"},
        )

        response = EquipmentDetailsResponse(equipment=equipment_data)

        equipment = Equipment(response)
        result = equipment.as_dict()

        expected = {
            "id": 1,
            "name": "Test Equipment",
            "description": "Test Description",
            "instruction_manual_file_name": "manual.pdf",
            "created_timestamp": datetime(2025, 3, 23),
            "userfields": {"custom_field": "custom_value"},
        }
        assert result == expected

    @pytest.mark.vcr
    def test_get_equipment_list(self, grocy: Grocy):
        equipment = grocy.equipment(get_details=False)

        assert isinstance(equipment, list)
        assert len(equipment) == 2
        for item in equipment:
            assert isinstance(item, Equipment)
            assert isinstance(item.id, int)
            assert isinstance(item.name, str)

        item = next(e for e in equipment if e.id == 1)
        assert item.name == "Coffee machine"
        assert item.instruction_manual_file_name == "loremipsum.pdf"

    @pytest.mark.vcr
    def test_get_equipment_with_details(self, grocy: Grocy):
        equipment = grocy.equipment(get_details=True)

        assert len(equipment) == 2

        item = next(e for e in equipment if e.id == 1)
        assert item.name == "Coffee machine"
        assert item.description is not None
        assert item.instruction_manual_file_name == "loremipsum.pdf"
        assert isinstance(item.created_timestamp, datetime)
        assert item.userfields is None

        dishwasher = next(e for e in equipment if e.id == 2)
        assert dishwasher.name == "Dishwasher"
        assert dishwasher.instruction_manual_file_name is None

    @pytest.mark.vcr
    def test_get_equipment_details(self, grocy: Grocy):
        equipment = grocy.get_equipment(1)

        assert isinstance(equipment, Equipment)
        assert equipment.id == 1
        assert equipment.name == "Coffee machine"
        assert equipment.description is not None
        assert equipment.description.startswith("<h1>Lorem ipsum")
        assert equipment.instruction_manual_file_name == "loremipsum.pdf"
        assert isinstance(equipment.created_timestamp, datetime)
        assert equipment.userfields is None

    @pytest.mark.vcr
    def test_get_equipment_details_non_existent(self, grocy: Grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.get_equipment(999)

        error = exc_info.value
        assert error.status_code == 400

    @pytest.mark.vcr
    def test_get_equipment_filters_valid(self, grocy: Grocy):
        query_filter = ["name=Coffee machine"]
        equipment = grocy.equipment(query_filters=query_filter)

        assert len(equipment) == 1
        assert equipment[0].name == "Coffee machine"

    @pytest.mark.vcr
    def test_get_equipment_filters_invalid(self, grocy: Grocy, invalid_query_filter):
        with pytest.raises(GrocyError) as exc_info:
            grocy.equipment(query_filters=invalid_query_filter)

        error = exc_info.value
        assert error.status_code == 500
