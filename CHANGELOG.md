# Changelog

## [1.0.1](https://github.com/iamkarlson/grocy-py/tree/1.0.1) (2026-08-28)

**Fixed**

- The four stock write paths that take a `best_before_date` now accept a plain `datetime.date`, not only a `datetime`. `StockManager.add` happened to work already because it formatted the value directly; `inventory`, `add_by_barcode` and `inventory_by_barcode` routed it through `localize_datetime()`, which reads `.tzinfo` and therefore raised `AttributeError: 'datetime.date' object has no attribute 'tzinfo'`. This is the type Home Assistant's `cv.date` validator produces, so it is the common case for downstream integrations.
- All four paths now share one date formatter, so they agree on the rendered value. Previously `add_product` skipped the localization step the other three applied; since `localize_datetime()` only attaches tzinfo and never shifts the clock, the emitted `YYYY-MM-DD` was already identical — the inconsistency was latent, not visible.

**Changed**

- `best_before_date` parameters are annotated `date | datetime | None` across `StockManager.add`, `.inventory`, `.add_by_barcode`, `.inventory_by_barcode` and the corresponding `GrocyApiClient` methods. Widening only; every call that type-checked against 1.0.0 still does. Inbound response models keep `datetime`, since Grocy returns timestamps there.

## [1.0.0](https://github.com/iamkarlson/grocy-py/tree/1.0.0) (2026-08-14)

First stable release. From here the package follows [semantic versioning](https://semver.org/) — see [Stability](README.md#stability) for exactly what that covers. Nothing was removed or renamed relative to 0.1.0, so this is a drop-in upgrade; the version number marks the commitment, not a break.

**Added**

- `StockManager.volatile(due_soon_days=None)` returns the raw `CurrentVolatileStockResponse` with all four buckets (due, overdue, expired, missing) in a single request, instead of one request per bucket.
- `StockManager.due_products(due_soon_days=...)` and `GrocyApiClient.get_volatile_stock(due_soon_days=...)`. Grocy defaults the due-soon window to 5 days and ignores the `stock_due_soon_days` system setting unless `?due_soon_days=N` is sent; there was previously no public way to send it, which pushed downstream consumers into calling the private API client.
- `Chore.period_interval`, `Chore.start_date`, `Chore.consume_product_on_execution` and `Chore.product_id`, populated from the chore responses ([#12](https://github.com/iamkarlson/grocy-py/pull/12) by @asylumfunk).
- `ChoreLogManager` is now exported from `grocy` and `grocy.managers`. It shipped in 0.1.0 as `grocy.chores_log` but was missing from both `__all__` lists.
- `EntityType` and `TransactionType` are re-exported from the package root.

**Fixed**

- `Grocy.chores_log` was annotated as returning `ChoreManager` instead of `ChoreLogManager`.
- Eight `GrocyApiClient` parameters used implicit `Optional` (`x: int = None`) and are now annotated `x: int | None = None`. Annotation-only; runtime behaviour is unchanged.
- `GrocyApiClient.get_volatile_stock()` raised `TypeError` on an empty response body and now returns an empty `CurrentVolatileStockResponse`.

**Changed**

- Runtime floor `requests>=2.33` for CVE-2026-25645 (insecure temp file reuse in `extract_zipped_paths`). Dev dependency `urllib3` relaxed from `==2.7.0` to `>=2.7.0` so future fixes are not blocked by an equality pin.
- Tested on Python 3.12, 3.13 and 3.14. `requires-python` stays `>=3.12`.
- The ruff rule set is now declared explicitly rather than inherited from ruff's defaults, so a ruff upgrade can no longer silently change what is enforced.

**Removed**

- Dead config inherited from the pygrocy2 fork: `tox.ini` (referenced requirements files that do not exist), `.flake8`, `stackaid.json`, `setup.py`, and the Probot-era `.github/stale.yml` / `.github/no-response.yml`. Dependabot is replaced by Renovate.

---

## [0.1.0](https://github.com/iamkarlson/grocy-py/tree/0.1.0) (2026-05-11)

First post-`0.0.x` release. Cleans up the long-standing PR backlog from forks and tightens runtime dependency pins for downstream consumers (notably the [Home Assistant Grocy integration](https://github.com/iamkarlson/grocy)).

**Added**

- `chores_log` manager: list and get individual chore log entries, with related `ChoreLog` data model that can populate the associated `Chore` and `User` via `get_details`. Includes new `ChoreLogResponse` / `ChoreLogManager` and corresponding tests + cassettes ([#5](https://github.com/iamkarlson/grocy-py/pull/5) by @lu-kno).
- `Product.location_id` field, populated from stock, details, and product-data responses ([#8](https://github.com/iamkarlson/grocy-py/pull/8) by @detobel36).
- `Product.picture_file_name` field, populated from the product-details response ([#10](https://github.com/iamkarlson/grocy-py/pull/10) by @Finnlife).
- `EntityType` enum coverage extended with `battery_charge_cycles`, `chores_log`, `meal_plan_sections`, `permission_hierarchy`, `product_barcodes_view`, `products_average_price`, `products_last_purchased`, `quantity_unit_conversions_resolved`, `recipes_pos_resolved`, `stock`, `stock_current_locations`, and `stock_log` ([#4](https://github.com/iamkarlson/grocy-py/pull/4) by @detobel36).
- `ruff` added to the dev dependency group.

**Changed**

- `EntityType` enum members renamed: `USER_FIELDS` → `USERFIELDS`, `USER_ENTITIES` → `USERENTITIES`, `USER_OBJECTS` → `USEROBJECTS` to match Grocy's exact endpoint names ([#4](https://github.com/iamkarlson/grocy-py/pull/4)). **Breaking** for consumers using the old constant names.
- Runtime dependency pins tightened with floor + major-version ceilings: `requests>=2.32,<3`, `tzdata>=2024.1`. `pydantic>=2.12.2,<2.14.0` retained (pydantic ships breaking changes in minors). `tzlocal~=5.2` unchanged.
- Dev dependency `responses` upper bound bumped to `<0.27` ([#7](https://github.com/iamkarlson/grocy-py/pull/7)).
- Dev dependency `urllib3` pinned to `==2.7.0` for the urllib3 GHSA-mf9v-mfxr-j63j / GHSA-qccp-gfcp-xxvc security fixes ([#11](https://github.com/iamkarlson/grocy-py/pull/11)).

---

## [2.4.0](https://github.com/flipper/pygrocy2/tree/2.4.0) (2025-01-09)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v2.2.0...2.4.0)

**Merged pull requests:**

- fix: set default value None for optional fields so we do not get validation error when the field is missing [\#2](https://github.com/flipper/pygrocy2/pull/2) ([umglurf](https://github.com/umglurf))

## [v2.2.0](https://github.com/flipper/pygrocy2/tree/v2.2.0) (2024-12-23)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v2.1.0...v2.2.0)

## [v2.1.0](https://github.com/flipper/pygrocy2/tree/v2.1.0) (2024-04-23)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v2.0.0...v2.1.0)

## [v2.0.0](https://github.com/flipper/pygrocy2/tree/v2.0.0) (2023-08-17)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v1.5.0...v2.0.0)

## [v1.5.0](https://github.com/flipper/pygrocy2/tree/v1.5.0) (2022-09-19)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v1.4.1...v1.5.0)

## [v1.4.1](https://github.com/flipper/pygrocy2/tree/v1.4.1) (2022-07-28)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v1.4.0...v1.4.1)

## [v1.4.0](https://github.com/flipper/pygrocy2/tree/v1.4.0) (2022-07-24)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v1.3.0...v1.4.0)

## [v1.3.0](https://github.com/flipper/pygrocy2/tree/v1.3.0) (2022-06-05)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v1.2.1...v1.3.0)

## [v1.2.1](https://github.com/flipper/pygrocy2/tree/v1.2.1) (2022-05-21)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v1.2.0...v1.2.1)

## [v1.2.0](https://github.com/flipper/pygrocy2/tree/v1.2.0) (2022-05-16)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v1.1.0...v1.2.0)

## [v1.1.0](https://github.com/flipper/pygrocy2/tree/v1.1.0) (2022-03-05)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v1.0.0...v1.1.0)

## [v1.0.0](https://github.com/flipper/pygrocy2/tree/v1.0.0) (2021-09-10)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.30.0...v1.0.0)

## [v0.30.0](https://github.com/flipper/pygrocy2/tree/v0.30.0) (2021-08-23)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.29.0...v0.30.0)

## [v0.29.0](https://github.com/flipper/pygrocy2/tree/v0.29.0) (2021-03-03)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.28.0...v0.29.0)

## [v0.28.0](https://github.com/flipper/pygrocy2/tree/v0.28.0) (2021-02-20)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.27.0...v0.28.0)

## [v0.27.0](https://github.com/flipper/pygrocy2/tree/v0.27.0) (2021-02-15)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.26.0...v0.27.0)

## [v0.26.0](https://github.com/flipper/pygrocy2/tree/v0.26.0) (2021-02-13)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.25.0...v0.26.0)

## [v0.25.0](https://github.com/flipper/pygrocy2/tree/v0.25.0) (2021-02-10)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.24.1...v0.25.0)

## [v0.24.1](https://github.com/flipper/pygrocy2/tree/v0.24.1) (2020-11-16)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.24.0...v0.24.1)

## [v0.24.0](https://github.com/flipper/pygrocy2/tree/v0.24.0) (2020-11-16)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.23.0...v0.24.0)

## [v0.23.0](https://github.com/flipper/pygrocy2/tree/v0.23.0) (2020-09-11)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.22.0...v0.23.0)

## [v0.22.0](https://github.com/flipper/pygrocy2/tree/v0.22.0) (2020-09-07)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.21.0...v0.22.0)

## [v0.21.0](https://github.com/flipper/pygrocy2/tree/v0.21.0) (2020-08-18)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.20.0...v0.21.0)

## [v0.20.0](https://github.com/flipper/pygrocy2/tree/v0.20.0) (2020-08-16)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.19.0...v0.20.0)

## [v0.19.0](https://github.com/flipper/pygrocy2/tree/v0.19.0) (2020-08-14)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.18.0...v0.19.0)

## [v0.18.0](https://github.com/flipper/pygrocy2/tree/v0.18.0) (2020-08-14)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.17.0...v0.18.0)

## [v0.17.0](https://github.com/flipper/pygrocy2/tree/v0.17.0) (2020-08-14)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.16.0...v0.17.0)

## [v0.16.0](https://github.com/flipper/pygrocy2/tree/v0.16.0) (2020-08-13)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.15.0...v0.16.0)

## [v0.15.0](https://github.com/flipper/pygrocy2/tree/v0.15.0) (2020-05-25)

[Full Changelog](https://github.com/flipper/pygrocy2/compare/v0.14.0...v0.15.0)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
