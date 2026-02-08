# API Response Types

These are Pydantic `BaseModel` classes used to deserialize raw JSON responses from the Grocy API. They are used internally by `GrocyApiClient` and passed to the higher-level data model classes.

You typically don't construct these directly, but they document the shape of the API responses.

## Stock Responses

::: grocy.grocy_api_client.CurrentStockResponse

::: grocy.grocy_api_client.ProductDetailsResponse

::: grocy.grocy_api_client.MissingProductResponse

::: grocy.grocy_api_client.StockLogResponse

## Product Data

::: grocy.grocy_api_client.ProductData

::: grocy.grocy_api_client.ProductBarcodeData

::: grocy.grocy_api_client.QuantityUnitData

::: grocy.grocy_api_client.LocationData

## Chore Responses

::: grocy.grocy_api_client.CurrentChoreResponse

::: grocy.grocy_api_client.ChoreDetailsResponse

::: grocy.grocy_api_client.ChoreData

## Task Responses

::: grocy.grocy_api_client.TaskResponse

::: grocy.grocy_api_client.TaskCategoryDto

## Battery Responses

::: grocy.grocy_api_client.CurrentBatteryResponse

::: grocy.grocy_api_client.BatteryDetailsResponse

::: grocy.grocy_api_client.BatteryData

## Equipment Responses

::: grocy.grocy_api_client.EquipmentDetailsResponse

::: grocy.grocy_api_client.EquipmentData

## Meal Plan Responses

::: grocy.grocy_api_client.MealPlanResponse

::: grocy.grocy_api_client.MealPlanSectionResponse

::: grocy.grocy_api_client.RecipeDetailsResponse

## Shopping List

::: grocy.grocy_api_client.ShoppingListItem

## User

::: grocy.grocy_api_client.UserDto

## System

::: grocy.grocy_api_client.SystemInfoDto

::: grocy.grocy_api_client.SystemTimeDto

::: grocy.grocy_api_client.SystemConfigDto

::: grocy.grocy_api_client.GrocyVersionDto
