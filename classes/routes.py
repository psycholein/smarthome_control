import json

class Routes:

  def __init__(self):
    self.routes = []

  def addRoute(self, path, obj, method):
    self.routes.append({
      'path':   path,
      'class':  obj,
      'method': method
    })

  def findRoute(self, data):
    if not type(data) is dict:
      try:
        data = json.loads(data)
      except:
        return None

    for route in self.routes:
      if data.get('path') == route.get('path'):
        route['params'] = {}
        if data.get('params'):
          for param in data.get('params'):
            route['params'][param] = data.get(param)
        else:
          route['params'] = data.get('values')
        return route
    return None
