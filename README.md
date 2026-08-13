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
| Chore Log | `grocy.chores_log` | Read individual chore execution log entries |
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

## Stability

From 1.0.0 this library follows [semantic versioning](https://semver.org/).

**What is covered.** Everything exported from the `grocy` package — `Grocy`,
the manager classes, `EntityType`, `TransactionType` — plus any name reachable
through a submodule path that does not start with an underscore, such as the
data models in `grocy.data_models`.

Within that surface:

- a **major** bump may remove or rename things, or change a signature
  incompatibly;
- a **minor** bump only adds;
- a **patch** bump only fixes behaviour.

**What is not covered.** `GrocyApiClient` and its `_do_get_request` /
`_do_post_request` / `_do_put_request` / `_do_delete_request` methods are
internal. They are deliberately not re-exported from the package root and may
change in any release. If you find yourself reaching for them because the
managers cannot express what you need, please open an issue — that is a gap
worth filling with public API instead.

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
