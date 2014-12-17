import threading, thread

class Dispatcher(threading.Thread):
  def __init__(self, app):
    super(self.__class__, self).__init__()
    self.app      = app
    self.commands = []
    self.running  = False
    self.process  = threading.Event()
    self.work     = threading.Event()

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
      self.app._dispatch(command)

    self.process.clear()
    return self.running

  def send(self, command, client):
    self.work.clear()
    self.commands.insert(0, command)
    self.work.set()
    self.process.set()

  def client_connected(self, client):
    self.send('client_connected', client)

  def client_disconnected(self, client):
    self.send('client_disconnected', client)
