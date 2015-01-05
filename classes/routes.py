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
    print "find route"
    try:
      data = json.loads(data)
    except:
      return None

    for route in self.routes:
      if data.get('path') == route.get('path'):
        route['values'] = data.get('values')
        return route
    return None
