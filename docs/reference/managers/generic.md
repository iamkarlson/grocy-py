# Generic Entity Manager

CRUD operations for any Grocy entity type. Use `EntityType` for type safety.

Access via `grocy.generic`.

```python
from grocy.data_models.generic import EntityType

# List, get, create, update, delete
locations = grocy.generic.list(EntityType.LOCATIONS)
loc = grocy.generic.get(EntityType.LOCATIONS, object_id=2)
grocy.generic.create(EntityType.LOCATIONS, {"name": "Pantry"})
grocy.generic.update(EntityType.LOCATIONS, object_id=2, data={"name": "Updated"})
grocy.generic.delete(EntityType.LOCATIONS, object_id=2)

# Custom user fields
fields = grocy.generic.get_userfields("products", object_id=1)
grocy.generic.set_userfields("products", object_id=1, key="my_field", value="value")
```

## Class Reference

::: grocy.managers.generic.GenericEntityManager
    options:
      members_order: source
      show_source: false
