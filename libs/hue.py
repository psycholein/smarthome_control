import threading
from phue import Bridge

class Hue(threading.Thread):

  def __init__(self, ip):
    threading.Thread.__init__(self)
    self.bridge = Bridge(ip)
    self.bridge.connect()

    self.process  = threading.Event()
    self.running  = True
    self.commands = []

  def run(self):
    while self._dispatch():
      self.process.wait()

  def stop(self):
    self.running = False
    self.process.set()

  def do(self, command):
    self.commands.insert(0, command)
    self.process.set()

  def _dispatch(self):
    while len(self.commands) > 0 and self.running:
      command = self.commands.pop()
      self.bridge.set_light(command.get('light'), command.get('cmd'), command.get('val'))

    self.process.clear()
    return self.running
