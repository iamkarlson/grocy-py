# User Manager

Manage users and user settings — list, get, create, edit, delete.

Access via `grocy.users`.

```python
# Current user
me = grocy.users.current()
print(f"Logged in as: {me.username}")

# All users
for user in grocy.users.list():
    print(f"{user.id}: {user.username}")

# User settings
settings = grocy.users.settings()
grocy.users.set_setting("my_key", "my_value")
```

## Class Reference

::: grocy.managers.users.UserManager
    options:
      members_order: source
      show_source: false
