# System Manager

Query system information — version, time, configuration, and database state.

Access via `grocy.system`.

```python
info = grocy.system.info()
print(f"Grocy {info.grocy_version}")

time = grocy.system.time()
print(f"Server time: {time.time_utc}")
```

## Class Reference

::: grocy.managers.system.SystemManager
    options:
      members_order: source
      show_source: false
