# Shopping List Manager

Manage shopping list items — view, add/remove products, and bulk operations.

Access via `grocy.shopping_list`.

```python
items = grocy.shopping_list.items(get_details=True)
for item in items:
    print(f"{item.product.name}: {item.amount}")

grocy.shopping_list.add_product(product_id=1, amount=3)
grocy.shopping_list.add_missing_products()
```

## Class Reference

::: grocy.managers.shopping_list.ShoppingListManager
    options:
      members_order: source
      show_source: false
