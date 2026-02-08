# Stock Manager

Manage product stock — query, add, consume, open, transfer, and inventory products.

Access via `grocy.stock`.

```python
# Get all products currently in stock
for product in grocy.stock.current():
    print(f"{product.name}: {product.available_amount}")

# Add, consume, open
grocy.stock.add(product_id=1, amount=5, price=2.99)
grocy.stock.consume(product_id=1, amount=1)
grocy.stock.open(product_id=1)
```

## Class Reference

::: grocy.managers.stock.StockManager
    options:
      members_order: source
      show_source: false
