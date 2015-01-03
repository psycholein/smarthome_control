import threading

class Fhem(threading.Thread):

  prefix = "/fhem?cmd=jsonlist2&XHR=1"

  def __init__(self, ip, port, dispatcher = None):
    threading.Thread.__init__(self)
    self.ip         = ip
    self.port       = port
    self.dispatcher = dispatcher
    self.work       = threading.Event()

  def run(self):
    self.running = True
    while self.getData():
      self.work.wait(60)

  def stop(self):
    self.running = False
    self.work.set()

  def getData(self):
    self.work.clear()
    return self.running
