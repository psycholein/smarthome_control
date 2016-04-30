import threading, thread, json

class Dispatcher(threading.Thread):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.routes   = {}
    self.commands = []
    self.running  = False
    self.process  = threading.Event()
    self.work     = threading.Event()

  def addRoute(self, path, func):
    self.routes[path] = func

  def run(self):
    self.running = True
    while self._dispatch():
      self.process.wait()

  def stop(self):
    self.running = False
    self.process.set()

  def decode(self, data):
    if not type(data) is dict:
      try:
        data = json.loads(data)
      except ValueError as e:
        if isinstance(data, basestring): return (data, None)
        return (None, None)

    path = data.get('path')
    params = {}
    if data.get('params'):
      for param in data.get('params'):
        params[param] = data.get(param)
    else:
      params = data.get('values')
    return (path, params)

  def _dispatch(self):
    while len(self.commands) > 0 and self.running:
      self.work.wait()
      path, params = self.decode(self.commands.pop())
      if path and self.routes.has_key(path):
        self.routes[path](params)

    self.process.clear()
    return self.running

  def send(self, command, client = None):
    self.work.clear()
    self.commands.insert(0, command)
    self.work.set()
    self.process.set()

  def clientConnected(self, client):
    self.send('client_connected', client)

  def clientDisconnected(self, client):
    self.send('client_disconnected', client)
