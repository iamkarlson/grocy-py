"""Public package interface for grocy.

Everything re-exported here is covered by the semantic-versioning promise in
the README. Names reachable only through a submodule path are supported too,
provided they do not start with an underscore.

`GrocyApiClient` and its `_do_*_request` methods are internal. They are not
re-exported and may change in any release; use the managers on `Grocy`.
"""

from .data_models.generic import EntityType
from .grocy import Grocy
from .grocy_api_client import TransactionType
from .managers import (
    BatteryManager,
    CalendarManager,
    ChoreLogManager,
    ChoreManager,
    EquipmentManager,
    FileManager,
    GenericEntityManager,
    MealPlanManager,
    RecipeManager,
    ShoppingListManager,
    StockManager,
    SystemManager,
    TaskManager,
    UserManager,
)

__all__ = [
    "BatteryManager",
    "CalendarManager",
    "ChoreLogManager",
    "ChoreManager",
    "EntityType",
    "EquipmentManager",
    "FileManager",
    "GenericEntityManager",
    "Grocy",
    "MealPlanManager",
    "RecipeManager",
    "ShoppingListManager",
    "StockManager",
    "SystemManager",
    "TaskManager",
    "TransactionType",
    "UserManager",
]

name = "grocy"
