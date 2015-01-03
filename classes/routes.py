class Routes:
  routes = {}

  def addRoute(self, path, obj, method):
    Routes.routes[hash(path)] = {
      'path':   path,
      'object': obj,
      'method': method
    }
    pass

  def findRoute(self, path):
    if Routes.routes.has_key(hash(path)): Routes.routes[path]
    return None
