# Chore Log Manager

Manage logged executions of household chores — list and get.

Access via `grocy.chores_log`.

```python
for chore_log in grocy.chores_log.list(get_details=True):
    print(f"{chore_log.chore.name} - execution time: {chore_log.tracked_time} by {chore_log.done_by_user.display_name")

```

## Class Reference

::: grocy.managers.chores_log.ChoreLogManager
    options:
      members_order: source
      show_source: false
