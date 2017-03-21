# Accessible Library

## Summary
API that wraps around platform accessibility APIs, can be used to retrieve information and modify behaviour of accessible objects.

## Interfaces
- IAccessible (Supported)
- IAccessible2 (Supported)
- ATSPI (Not Supported)
- ATK (Not Supported)

## Installation
```
pip install -r requirements.txt
```

## Usage
```
python AccessibilityAPIServer.py [port-number]
```

## API Reference
### Accessible Object

Retrieve accesible object information

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

Track event on accessible

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

Run command on accessible object

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
 
## Tests

```
python test_IAccessible.py
```






