# Errors

Exception classes raised by the library.

## GrocyError

Raised when the Grocy API returns an HTTP 4xx or 5xx response.

```python
from grocy.errors import GrocyError

try:
    product = grocy.product(99999)
except GrocyError as e:
    print(f"HTTP {e.status_code}: {e.message}")
```

::: grocy.errors.grocy_error.GrocyError
    options:
      members_order: source
