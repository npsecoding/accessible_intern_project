# Accessible Library

## Summary
API that wraps around platform accessibility APIs, can be used to retrieve information and modify behaviour of accessible objects.

## Interfaces
- IAccessible (Supported)
- IAccessible2 (Supported)
- ATSPI (Not Supported)
- ATK (Not Supported)

## Installation
Install accessible library dependencies.

```
pip install -r requirements.txt
```

## Usage
Launch Accessible API service.

**Required:**
port number
application

**Optional:**

platform

verbose

```
python AccessibilityAPIServer.py [port number] [application] [platform] [verbose]
```

## API Reference
### Accessible Object

Retrieve accesible object information.

- URL:

  /accessible

- METHOD:

  GET

- URL PARAMS:

  **Required:**

  interface=[string]

  **Optional:**

  name=[string]

  role=[integer]

  depth=[integer]

### Event

Track event on accessible.

- URL:

  /event

- METHOD:

  GET

- URL PARAMS:

  **Required:**

  interface=[string]

  type=[string]

  **Optional:**

  name=[string]

  role=[integer]

### Command

Run command on accessible object.

- URL:

  /cmd

- METHOD:

  GET

- URL PARAMS:

  **Required:**

  interface=[string]

  function=[string]

  param=[primitive]

  **Optional:**

  name=[string]

  role=[integer]

## Platform Tests

### Summary
Marionette will drive the Gecko Web Engine in Firefox.

### Setup
Install Mozilla's automation engine, check out the docs here: [Marionette Docs](http://marionette-client.readthedocs.io/en/master/index.html)

```
pip install marionette_driver
```

### Example
Simple test that gets an accessible checkbox object, listens for the check event on the checkbox and compares resulting state.

```
python test_IAccessible.py
```






