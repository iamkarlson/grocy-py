import datetime

import pytest

from grocy.data_models.meal_items import (
    MealPlanItemType,
    MealPlanSection,
    RecipeItem,
)
from grocy.errors import GrocyError


class TestMealPlan:
    @pytest.mark.vcr
    def test_get_meal_plan_valid(self, grocy):
        meal_plan = grocy.meal_plan.items(get_details=False)

        assert len(meal_plan) == 12
        item = next(item for item in meal_plan if item.id == 1)
        assert item.day.day == 5
        assert item.recipe_id == 1
        assert item.recipe_servings == 1
        assert item.note is None
        assert item.recipe is None

    @pytest.mark.vcr
    def test_get_meal_plan_with_details_valid(self, grocy):
        meal_plan = grocy.meal_plan.items(get_details=True)

        assert len(meal_plan) == 12
        item = next(item for item in meal_plan if item.id == 1)
        assert item.day.day == 5
        assert item.recipe_id == 1
        assert item.recipe_servings == 1
        assert item.note is None
        assert isinstance(item.recipe, RecipeItem)

        recipe = item.recipe
        assert recipe.name == "Pizza"
        assert recipe.id == 1
        assert recipe.desired_servings == 1
        assert recipe.base_servings == 1
        assert recipe.description[:4] == "<h1>"
        assert recipe.picture_file_name == "pizza.jpg"

        section_item = next(item for item in meal_plan if item.section_id == 1)
        assert isinstance(section_item.section, MealPlanSection)

    @pytest.mark.vcr
    def test_get_meal_plan_with_note_and_details(self, grocy):
        meal_plan = grocy.meal_plan.items(get_details=True)

        note_entry = next(
            item for item in meal_plan if item.type == MealPlanItemType.NOTE
        )
        assert note_entry.note == "This is a note"

    @pytest.mark.vcr
    def test_get_meal_plan_with_product(self, grocy):
        meal_plan = grocy.meal_plan.items(get_details=True)

        product_entry = next(
            item for item in meal_plan if item.type == MealPlanItemType.PRODUCT
        )
        assert product_entry.product_id == 3

    @pytest.mark.vcr
    def test_get_meal_plan_filters_valid(self, grocy):
        query_filter = ["day>=2022-06-15", "product_amount>0"]
        meal_plans = grocy.meal_plan.items(get_details=True, query_filters=query_filter)

        for item in meal_plans:
            assert item.day >= datetime.date(2022, 6, 15)

    @pytest.mark.vcr
    def test_get_meal_plan_filters_invalid(self, grocy, invalid_query_filter):
        with pytest.raises(GrocyError) as exc_info:
            grocy.meal_plan.items(get_details=True, query_filters=invalid_query_filter)

        error = exc_info.value
        assert error.status_code == 500


class TestMealPlanItemType:
    """Grocy stores meal_plan.type as free text without a constraint (#69 in iamkarlson/grocy)."""

    @staticmethod
    def _response(type_value: str):
        from grocy.grocy_api_client import MealPlanResponse

        return MealPlanResponse(
            id=7,
            day="2026-10-03 00:00:00",
            type=type_value,
            row_created_timestamp="2026-10-01 12:00:00",
        )

    @pytest.mark.parametrize("member", list(MealPlanItemType))
    def test_known_type_is_enum_member(self, member, caplog):
        from grocy.data_models.meal_items import MealPlanItem

        item = MealPlanItem.from_response(self._response(member.value))

        assert item.type is member
        assert "unknown type" not in caplog.text

    @pytest.mark.parametrize("value", ["main", "side"])
    def test_main_and_side_are_known(self, value):
        from grocy.data_models.meal_items import MealPlanItem

        item = MealPlanItem.from_response(self._response(value))

        assert isinstance(item.type, MealPlanItemType)
        assert item.type == value

    def test_unknown_type_is_kept_as_string(self, caplog):
        from grocy.data_models.meal_items import MealPlanItem

        item = MealPlanItem.from_response(self._response("dessert"))

        assert item.type == "dessert"
        assert not isinstance(item.type, MealPlanItemType)
        assert "Meal plan item 7 has unknown type 'dessert'" in caplog.text
