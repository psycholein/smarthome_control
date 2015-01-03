class Routes:

  def __init__(self):
    self.routes = []

  def addRoute(self, path, obj, method):
    self.routes.append({
      'path':   path,
      'object': obj,
      'method': method
    })

  def findRoute(self, path):
    for route in self.routes:
      pass
    return None
