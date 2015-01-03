import threading, thread

class Events(threading.Thread):
  def __init__(self, dispatcher = None):
    super(self.__class__, self).__init__()
    self.dispatcher = dispatcher
    self.running    = False
    self.events     = []
    self.work       = threading.Event()

  def addEvent(self, typ, command, values):
    self.events.append({
        'typ':     typ,
        'command': command,
        'value':   value,
        'status':  None
      })

  def run(self):
    self.running = True
    while self.check():
      self.work.wait(60)

  def check(self):
    self.work.clear()
    return self.running

  def stop(self):
    self.running = False
    self.work.set()

  def trigger(self, typ, command, values):
    pass
