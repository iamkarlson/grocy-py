# Battery Manager

Track battery charge cycles — list, get details, charge, and undo.

Access via `grocy.batteries`.

```python
for battery in grocy.batteries.list(get_details=True):
    print(f"{battery.name}: last charged {battery.last_charged}")

grocy.batteries.charge(battery_id=1)
```

## Class Reference

::: grocy.managers.batteries.BatteryManager
    options:
      members_order: source
      show_source: false
