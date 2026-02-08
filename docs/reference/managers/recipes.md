# Recipe Manager

Manage recipes — get details, check fulfillment, consume, and copy.

Access via `grocy.recipes`.

```python
recipe = grocy.recipes.get(recipe_id=1)
print(f"{recipe.name}: {recipe.base_servings} servings")

# Check what's missing
fulfillment = grocy.recipes.fulfillment(recipe_id=1)
print(f"Fulfilled: {fulfillment.need_fulfilled}")

# Add missing ingredients to shopping list
grocy.recipes.add_not_fulfilled_to_shopping_list(recipe_id=1)
```

## Class Reference

::: grocy.managers.recipes.RecipeManager
    options:
      members_order: source
      show_source: false
