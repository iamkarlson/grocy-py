# Chore Manager

Manage household chores — list, execute, undo, and assign.

Access via `grocy.chores`.

```python
for chore in grocy.chores.list(get_details=True):
    print(f"{chore.name} - next: {chore.next_estimated_execution_time}")

grocy.chores.execute(chore_id=1, done_by=1)
```

## Class Reference

::: grocy.managers.chores.ChoreManager
    options:
      members_order: source
      show_source: false
