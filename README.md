# grocy-py

A Python client library for the [Grocy](https://grocy.info/) ERP system API.

Check out the [documentation](https://iamkarlson.github.io/grocy-py/).

## Installation

```bash
pip install grocy-py
```

## Usage

```python
from grocy import Grocy

grocy = Grocy("https://example.com", "GROCY_API_KEY")
```

With custom port and SSL options:

```python
grocy = Grocy("https://example.com", "GROCY_API_KEY", port=9192, verify_ssl=True)
```

Get current stock:

```python
for product in grocy.stock.current():
    print(f"{product.name}: {product.available_amount} in stock")
```

## Features

All features are accessed through manager objects on the `Grocy` instance:

| Manager | Access | Description |
|---|---|---|
| Stock | `grocy.stock` | Query, add, consume, open, transfer products |
| Shopping List | `grocy.shopping_list` | View and manage shopping list items |
| Chores | `grocy.chores` | List, execute, and track chores |
| Tasks | `grocy.tasks` | Manage and complete tasks |
| Batteries | `grocy.batteries` | Track battery charge cycles |
| Equipment | `grocy.equipment` | Manage household equipment |
| Meal Plan | `grocy.meal_plan` | View meal plans and sections |
| Recipes | `grocy.recipes` | Get recipes, check fulfillment, consume |
| Users | `grocy.users` | Manage users and settings |
| System | `grocy.system` | Server info, time, config |
| Calendar | `grocy.calendar` | iCalendar export and sharing |
| Files | `grocy.files` | Upload, download, delete files |
| Generic | `grocy.generic` | CRUD any Grocy entity type |

## Development

```bash
# Install dependencies
uv sync --group dev

# Run tests
uv run pytest

# Lint and format
uv run ruff check .
uv run ruff format .

# Build docs
uv run mkdocs serve
```

## Support

If you need help using grocy check the [discussions](https://github.com/iamkarlson/grocy-py/issues) section. Feel free to create an issue for feature requests, bugs and errors in the library.
