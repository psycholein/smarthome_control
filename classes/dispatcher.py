import threading, thread

class Dispatcher(threading.Thread):
  def __init__(self, routes = None):
    super(self.__class__, self).__init__()
    self.routes   = routes
    self.commands = []
    self.running  = False
    self.process  = threading.Event()
    self.work     = threading.Event()
    self.objects  = {}

  def addDispatchObject(self, obj):
    self.objects[hash(obj)] = obj

  def run(self):
    self.running = True
    while self._dispatch():
      self.process.wait()

  def stop(self):
    self.running = False
    self.process.set()

  def _dispatch(self):
    while len(self.commands) > 0 and self.running:
      self.work.wait()
      command = self.commands.pop()
      obj = self.routes.findRoute(command)
      if obj:
        pass

    self.process.clear()
    return self.running

  def send(self, command, client):
    self.work.clear()
    self.commands.insert(0, command)
    self.work.set()
    self.process.set()

  def clientConnected(self, client):
    self.send('client_connected', client)

  def clientDisconnected(self, client):
    self.send('client_disconnected', client)
