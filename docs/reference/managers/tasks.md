# Task Manager

Manage tasks — list, get details, complete, and undo.

Access via `grocy.tasks`.

```python
for task in grocy.tasks.list():
    print(f"{task.name} - due: {task.due_date}")

grocy.tasks.complete(task_id=1)
```

## Class Reference

::: grocy.managers.tasks.TaskManager
    options:
      members_order: source
      show_source: false
