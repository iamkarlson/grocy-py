# grocy-py

A Python client library for the [Grocy](https://grocy.info/) ERP system API.

grocy provides a clean, typed Python interface to manage your household inventory — products, stock, shopping lists, chores, tasks, batteries, equipment, meal plans, and more.

## Quick Example

```python
from grocy import Grocy

grocy = Grocy("https://your-grocy-instance.com", "YOUR_API_KEY")

# Get current stock
for product in grocy.stock.current():
    print(f"{product.name}: {product.available_amount} in stock")

# Get overdue products
for product in grocy.stock.overdue_products():
    print(f"{product.name} is overdue!")

# Manage shopping list
shopping_list = grocy.shopping_list.items(get_details=True)
for item in shopping_list:
    print(f"{item.product.name}: {item.amount}")
```

## Features

- **[Stock](reference/managers/stock.md)** — query, add, consume, open, transfer, and inventory products
- **[Shopping lists](reference/managers/shopping_list.md)** — view, add/remove products, bulk operations
- **[Chores](reference/managers/chores.md)** — list, execute, undo, and assign chores
- **[Tasks](reference/managers/tasks.md)** — manage and complete tasks
- **[Batteries](reference/managers/batteries.md)** — track battery charge cycles
- **[Equipment](reference/managers/equipment.md)** — manage household equipment
- **[Recipes](reference/managers/recipes.md)** — get details, check fulfillment, consume
- **[Meal plans](reference/managers/meal_plan.md)** — view meal plans and sections
- **[Users](reference/managers/users.md)** — manage user accounts and settings
- **[System](reference/managers/system.md)** — server info, time, and configuration
- **[Calendar](reference/managers/calendar.md)** — iCalendar export and sharing
- **[Files](reference/managers/files.md)** — upload, download, and delete files
- **[Generic CRUD](reference/managers/generic.md)** — create, read, update, delete any entity type

## Architecture Overview

```
grocy
├── Grocy              # High-level client (you use this)
├── GrocyApiClient     # Low-level HTTP API wrapper
├── Data Models        # Rich domain objects (Product, Chore, Task, ...)
├── API Responses      # Pydantic models for raw API responses
├── Enums              # EntityType, TransactionType, etc.
└── Errors             # GrocyError exception
```

| Layer | Purpose |
|---|---|
| [`Grocy`](reference/grocy.md) | Main entry point. Methods return rich data model objects. |
| [`GrocyApiClient`](reference/api-responses.md) | Handles HTTP requests/responses. Returns Pydantic response models. |
| [Data Models](reference/models/product.md) | Domain classes like `Product`, `Chore`, `Task` with properties. |
| [API Responses](reference/api-responses.md) | Pydantic `BaseModel` classes for JSON deserialization. |
| [Enums](reference/enums.md) | `EntityType`, `TransactionType`, `PeriodType`, etc. |
| [Errors](reference/errors.md) | `GrocyError` raised on HTTP 4xx/5xx responses. |
