from __future__ import annotations

import base64
import logging
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel

_LOGGER = logging.getLogger(__name__)


class RecipeItem(BaseModel):
    """A recipe with serving information."""

    id: int | None = None
    name: str
    description: str | None = None
    base_servings: int
    desired_servings: int
    picture_file_name: str | None = None

    @classmethod
    def from_response(cls, resp) -> RecipeItem:
        """Create from a recipe API response."""
        return cls(
            id=resp.id,
            name=resp.name,
            description=resp.description,
            base_servings=resp.base_servings,
            desired_servings=resp.desired_servings,
            picture_file_name=resp.picture_file_name,
        )

    def get_picture_url_path(self, width: int = 400):
        """Build the API URL path for the recipe picture.

        Args:
            width: Desired image width in pixels.
        """
        if self.picture_file_name:
            b64name = base64.b64encode(self.picture_file_name.encode("ascii"))
            path = "files/recipepictures/" + str(b64name, "utf-8")
            return f"{path}?force_serve_as=picture&best_fit_width={width}"


class MealPlanSection(BaseModel):
    """A named section within the meal plan."""

    id: int | None = None
    name: str | None = None
    sort_number: int | None = None
    row_created_timestamp: datetime | None = None

    @classmethod
    def from_response(cls, resp) -> MealPlanSection:
        """Create from a meal plan section API response."""
        return cls(
            id=resp.id,
            name=resp.name,
            sort_number=resp.sort_number,
            row_created_timestamp=resp.row_created_timestamp,
        )


class MealPlanItemType(str, Enum):
    """Type of item in a meal plan entry."""

    NOTE = "note"
    PRODUCT = "product"
    RECIPE = "recipe"
    MAIN = "main"
    SIDE = "side"


class MealPlanItem(BaseModel):
    """A single entry in the meal plan."""

    id: int
    day: date | None = None
    recipe_id: int | None = None
    recipe_servings: int | None = None
    note: str | None = None
    recipe: RecipeItem | None = None
    section_id: int | None = None
    section: MealPlanSection | None = None
    # Grocy stores the type as free text, so values outside the enum are kept as-is.
    type: MealPlanItemType | str
    product_id: int | None = None

    @classmethod
    def from_response(cls, resp) -> MealPlanItem:
        """Create from a meal plan API response."""
        day = cls._normalize_day(resp.day)
        return cls(
            id=resp.id,
            day=day,
            recipe_id=resp.recipe_id,
            recipe_servings=resp.recipe_servings,
            note=resp.note,
            section_id=resp.section_id,
            type=cls._parse_type(resp.type, resp.id),
            product_id=resp.product_id,
        )

    def get_details(self, api_client):
        """Fetch and populate linked recipe and section details from the API."""
        if self.recipe_id:
            recipe = api_client.get_recipe(self.recipe_id)
            if recipe:
                self.recipe = RecipeItem.from_response(recipe)
        if self.section_id:
            section = api_client.get_meal_plan_section(self.section_id)
            if section:
                self.section = MealPlanSection.from_response(section)

    @staticmethod
    def _parse_type(value: str, item_id: int) -> MealPlanItemType | str:
        try:
            return MealPlanItemType(value)
        except ValueError:
            _LOGGER.warning(
                "Meal plan item %s has unknown type %r; keeping it as a string",
                item_id,
                value,
            )
            return value

    @staticmethod
    def _normalize_day(value) -> date | None:
        if value is None:
            return None
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if isinstance(value, datetime):
            return value.date()
        return datetime.fromisoformat(str(value)).date()
