import threading
import requests

class Fhem(threading.Thread):

  prefix = "/fhem"
  json   = "?cmd=jsonlist2&XHR=1"
  temp   = "?room={room}&dev.{device}={device}&arg.{device}=desired-temp&val.{device}=25&cmd.{device}=set"

  def __init__(self, ip, port, dispatcher = None):
    threading.Thread.__init__(self)
    self.api        = "http://%s:%s%s" % (ip, port, self.prefix)
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
    if not self.running: return self.running

    self.work.clear()
    request = requests.get(self.api + self.json)
    if request.status_code != requests.codes.ok: return self.running

    data = None
    try:
      data = request.json()
    except:
      data = None
    if not data: return self.running

    self.analyzeData(data)

    return self.running

  def analyzeData(self, data):
    pass
