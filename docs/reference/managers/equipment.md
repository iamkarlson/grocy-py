# Equipment Manager

Manage household equipment — list, get by ID or name.

Access via `grocy.equipment`.

```python
for e in grocy.equipment.list(get_details=True):
    print(f"{e.name}: {e.description}")
```

## Class Reference

::: grocy.managers.equipment.EquipmentManager
    options:
      members_order: source
      show_source: false
