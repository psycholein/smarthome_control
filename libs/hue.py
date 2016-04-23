import threading
from phue import Bridge

class Hue(threading.Thread):

  def __init__(self, ip, dispatcher = None):
    threading.Thread.__init__(self)
    self.bridge = Bridge(ip)
    self.bridge.connect()

    self.dispatcher = dispatcher
    self.process    = threading.Event()
    self.running    = True
    self.commands   = []
    self.dispatcher.addRoute("hue", self.do)

  def run(self):
    while self._dispatch():
      self.process.wait()

  def stop(self):
    self.running = False
    self.process.set()

  def do(self, command):
    self.commands.insert(0, command)
    self.process.set()

  def RGB2CIE(self, r, g, b):
    x = 0.4124*r + 0.3576*g + 0.1805*b
    y = 0.2126*r + 0.7152*g + 0.0722*b
    z = 0.0193*r + 0.1192*g + 0.9505*b
    return [x / (x + y + z), y / (x + y + z)]

  def _dispatch(self):
    while len(self.commands) > 0 and self.running:
      command = self.commands.pop()
      self.bridge.set_light(command.get('light'), command.get('cmd'), command.get('val'))

    self.process.clear()
    return self.running
