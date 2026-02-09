# Getting Started

## Installation

```bash
pip install grocy-py
```

## Requirements

- Python >= 3.12
- A running [Grocy](https://grocy.info/) instance with API access

## Connecting to Grocy

```python
from grocy import Grocy

# Basic connection
grocy = Grocy("https://your-grocy-instance.com", "YOUR_API_KEY")

# With custom port and path
grocy = Grocy(
    "https://your-grocy-instance.com",
    "YOUR_API_KEY",
    port=9192,
    path="grocy",       # if Grocy is behind a subpath
    verify_ssl=True,
    debug=False,
)
```

The `Grocy` class constructs the API URL as `{base_url}:{port}/api/` (or `{base_url}:{port}/{path}/api/` when a path is provided).

## Local Development with Docker

The repository includes a `docker-compose.yml` that spins up a Grocy demo instance with a pre-seeded API key, so you can start experimenting immediately.

**Start the instance:**

```bash
docker compose up -d
```

This launches Grocy in demo mode on `localhost:9192` and automatically inserts a
known API key (`test_local_devenv`) into the demo database.

**Connect to it:**

```python
from grocy import Grocy

grocy = Grocy("http://localhost", "test_local_devenv", port=9192)

for product in grocy.stock.current():
    print(f"{product.name}: {product.available_amount}")
```

!!! tip
    Check out the [Example Notebook](example.ipynb) for a runnable walkthrough
    you can open in Jupyter.

## Working with Stock

```python
# Current stock
stock = grocy.stock.current()
for product in stock:
    print(f"{product.name}: {product.available_amount}")

# Add product to stock
grocy.stock.add(product_id=1, amount=5, price=2.99)

# Consume a product
grocy.stock.consume(product_id=1, amount=1)

# Open a product
grocy.stock.open(product_id=1)

# Transfer between locations
grocy.stock.transfer(product_id=1, amount=1, location_from=1, location_to=2)

# Set exact inventory amount
grocy.stock.inventory(product_id=1, new_amount=10)

# Products that are due, overdue, expired, or missing
due = grocy.stock.due_products(get_details=True)
overdue = grocy.stock.overdue_products(get_details=True)
expired = grocy.stock.expired_products(get_details=True)
missing = grocy.stock.missing_products(get_details=True)

# Lookup by barcode
product = grocy.stock.product_by_barcode("4006381333931")

# Stock entries, locations, and price history for a product
entries = grocy.stock.product_entries(product_id=1)
locations = grocy.stock.product_locations(product_id=1)
prices = grocy.stock.product_price_history(product_id=1)

# Product groups
groups = grocy.stock.product_groups()
```

## Shopping Lists

```python
# Get shopping list items
items = grocy.shopping_list.items(get_details=True)
for item in items:
    print(f"{item.product.name}: {item.amount} (done: {item.done})")

# Add / remove products
grocy.shopping_list.add_product(product_id=1, amount=3)
grocy.shopping_list.remove_product(product_id=1, amount=1)

# Mark an item as done / not done
grocy.shopping_list.mark_item_done(shopping_list_item_id=1, done=True)
grocy.shopping_list.mark_item_done(shopping_list_item_id=1, done=False)

# Bulk operations
grocy.shopping_list.add_missing_products()
grocy.shopping_list.add_overdue_products()
grocy.shopping_list.add_expired_products()

# Clear the shopping list
grocy.shopping_list.clear()
```

## Chores

```python
# List all chores
chores = grocy.chores.list(get_details=True)
for chore in chores:
    print(f"{chore.name} - next: {chore.next_estimated_execution_time}")

# Get specific chore details
chore = grocy.chores.get(chore_id=1)

# Execute a chore
grocy.chores.execute(chore_id=1, done_by=1)

# Undo an execution
grocy.chores.undo(execution_id=1)

# Calculate next assignments
grocy.chores.calculate_next_assignments()
```

## Tasks

```python
# List tasks
tasks = grocy.tasks.list()
for task in tasks:
    print(f"{task.name} - due: {task.due_date}")

# Get a specific task
task = grocy.tasks.get(task_id=1)

# Complete / undo
grocy.tasks.complete(task_id=1)
grocy.tasks.undo(task_id=1)
```

## Batteries

```python
# List batteries
batteries = grocy.batteries.list(get_details=True)
for battery in batteries:
    print(f"{battery.name}: last charged {battery.last_charged}")

# Get a specific battery
battery = grocy.batteries.get(battery_id=1)

# Charge / undo
grocy.batteries.charge(battery_id=1)
grocy.batteries.undo(charge_cycle_id=1)
```

## Equipment

```python
# List all equipment
for e in grocy.equipment.list(get_details=True):
    print(f"{e.name}: {e.description}")

# Get by ID or name
e = grocy.equipment.get(equipment_id=1)
e = grocy.equipment.get_by_name("Coffee machine")
```

## Recipes

```python
# Get a recipe
recipe = grocy.recipes.get(recipe_id=1)
print(f"{recipe.name} ({recipe.base_servings} servings)")

# Check fulfillment
fulfillment = grocy.recipes.fulfillment(recipe_id=1)
print(f"Fulfilled: {fulfillment.need_fulfilled}, missing: {fulfillment.missing_products_count}")

# Get all recipes' fulfillment status
for f in grocy.recipes.all_fulfillment():
    print(f"Recipe {f.recipe_id}: fulfilled={f.need_fulfilled}")

# Add missing ingredients to shopping list
grocy.recipes.add_not_fulfilled_to_shopping_list(recipe_id=1)

# Consume recipe ingredients from stock
grocy.recipes.consume(recipe_id=1)

# Copy a recipe
grocy.recipes.copy(recipe_id=1)
```

## Meal Plans

```python
# Get meal plan items
meals = grocy.meal_plan.items(get_details=True)
for meal in meals:
    print(f"{meal.day}: {meal.recipe.name if meal.recipe else meal.note}")

# Get meal plan sections
sections = grocy.meal_plan.sections()
section = grocy.meal_plan.section(section_id=1)
```

## Users

```python
# Current user
me = grocy.users.current()
print(f"Logged in as: {me.username}")

# List all users
for user in grocy.users.list():
    print(f"{user.id}: {user.username}")

# Get a specific user
user = grocy.users.get(user_id=1)

# Create / edit / delete
grocy.users.create({"username": "newuser", "password": "secret"})
grocy.users.edit(user_id=2, data={"first_name": "Updated"})
grocy.users.delete(user_id=2)

# User settings
settings = grocy.users.settings()
grocy.users.set_setting("my_key", "my_value")
value = grocy.users.get_setting("my_key")
grocy.users.delete_setting("my_key")
```

## System

```python
# System information
info = grocy.system.info()
print(f"Grocy {info.grocy_version} on {info.os}")

# Server time
time = grocy.system.time()
print(f"UTC: {time.time_utc}, Timezone: {time.timezone}")

# Configuration
config = grocy.system.config()
print(f"Currency: {config.currency}, Features: {config.enabled_features}")

# Last database change
db_time = grocy.system.db_changed_time()
```

## Calendar

```python
# Get calendar in iCalendar format
ical = grocy.calendar.ical()

# Get a sharing link
link = grocy.calendar.sharing_link()
```

## Files

```python
# Upload a file
with open("photo.jpg", "rb") as f:
    grocy.files.upload(group="productpictures", file_name="photo.jpg", data=f)

# Download a file
data = grocy.files.download(group="productpictures", file_name="photo.jpg")

# Delete a file
grocy.files.delete(group="productpictures", file_name="photo.jpg")

# Convenience: upload a product picture
grocy.stock.upload_product_picture(product_id=1, pic_path="/path/to/photo.jpg")
```

## Generic CRUD Operations

For any Grocy entity type, you can use the generic CRUD methods:

```python
from grocy.data_models.generic import EntityType

# List all objects of a type
locations = grocy.generic.list(EntityType.LOCATIONS)

# Get a single object
location = grocy.generic.get(EntityType.LOCATIONS, object_id=2)

# Create
grocy.generic.create(EntityType.LOCATIONS, {"name": "Pantry"})

# Update
grocy.generic.update(EntityType.LOCATIONS, object_id=2, data={"name": "Kitchen Pantry"})

# Delete
grocy.generic.delete(EntityType.LOCATIONS, object_id=2)

# Custom user fields
fields = grocy.generic.get_userfields("products", object_id=1)
grocy.generic.set_userfields("products", object_id=1, key="my_field", value="value")
```

## The `get_details` Pattern

Many methods accept a `get_details=True` parameter. When enabled, each returned object makes an additional API call to fetch full details (name, barcodes, etc.). Without it, you only get the summary data from the list endpoint.

```python
# Summary only (1 API call)
stock = grocy.stock.current()

# Full details (1 + N API calls)
due = grocy.stock.due_products(get_details=True)
for product in due:
    print(product.name)       # available with details
    print(product.barcodes)   # available with details
```

## Error Handling

```python
from grocy.errors import GrocyError

try:
    grocy.stock.product(product_id=99999)
except GrocyError as e:
    print(f"HTTP {e.status_code}: {e.message}")
    if e.is_client_error:
        print("Client error (4xx)")
    elif e.is_server_error:
        print("Server error (5xx)")
```

## Debug Mode

Enable debug logging to see all HTTP requests and responses:

```python
grocy = Grocy("https://example.com", "API_KEY", debug=True)
```
