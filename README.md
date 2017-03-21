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
python server.py
```

## API Reference
### Accessible Object
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






