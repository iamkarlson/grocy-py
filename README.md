# grocy-py
Check out [source code reference docs](https://iamkarlson.github.io/grocy-py/)

## Installation

`pip install grocy-py`

## Usage

Import the package:

```python
from grocy import Grocy
```

Obtain a grocy instance:

```python
grocy = Grocy("https://example.com", "GROCY_API_KEY")
```

or

```python
grocy = Grocy("https://example.com", "GROCY_API_KEY", port = 9192, verify_ssl = True)
```

Get current stock:

```python
for entry in grocy.stock():
    print("{} in stock for product id {}".format(entry.available_amount, entry.id))
```

# Support

If you need help using grocy check the [discussions](https://github.com/iamkarlson/grocy-py/issues) section. Feel free to create an issue for feature requests, bugs and errors in the library.

## Development testing

You need tox and Python 3.13 to run the tests. Navigate to the root dir of `grocy` and execute `tox` to run the tests.
