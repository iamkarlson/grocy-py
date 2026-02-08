# Meal Plan Manager

View meal plan items and sections.

Access via `grocy.meal_plan`.

```python
for meal in grocy.meal_plan.items(get_details=True):
    name = meal.recipe.name if meal.recipe else meal.note
    print(f"{meal.day}: {name}")
```

## Class Reference

::: grocy.managers.meal_plan.MealPlanManager
    options:
      members_order: source
      show_source: false
