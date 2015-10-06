import threading, requests

from classes.values import Values

class Fhem(threading.Thread):

  prefix = "/fhem"
  json   = "?cmd=jsonlist2&XHR=1"
  temp   = "?dev.{device}={device}&arg.{device}=desired-temp&val.{device}={value}&cmd.{device}=set&XHR=1"

  def __init__(self, ip, port, dispatcher = None):
    threading.Thread.__init__(self)
    self.api        = "http://%s:%s%s" % (ip, port, self.prefix)
    self.dispatcher = dispatcher
    self.devices    = []
    self.callbacks  = []
    self.attributes = []
    self.work       = threading.Event()

  def run(self):
    self.running = True
    while self.getData():
      self.work.wait(60)

  def stop(self):
    self.running = False
    self.work.set()

  def addDevice(self, device):
    if device: self.devices.append(device)

  def addAttribute(self, attr):
    self.attributes.append(attr)

  def registerCallback(self, callback):
    self.callbacks.append(callback)

  def removeCallback(self, callback):
    self.callbacks.remove(callback)

  def triggerCallbacks(self, data):
    for callback in self.callbacks: callback(data)

  def getData(self):
    if not self.running: return self.running

    self.work.clear()
    try:
      request = requests.get(self.api + self.json)
    except:
      return self.running

    if request.status_code != requests.codes.ok: return self.running

    results = None
    try:
      results = request.json()
    except:
      pass

    if results: self.analyzeResults(results)
    return self.running

  def analyzeResults(self, results):
    for result in results.get('Results', []):
      name = result.get('Name')
      if name in self.devices:
        data     = {'id': name}
        readings = result.get('Readings')
        if not readings: continue
        for attr in self.attributes:
          value = readings.get(attr)
          if value: data[attr] = value.get('Value').strip()
        for callback in self.callbacks: callback(data)

  def setDesiredTemp(self, values):
    device = values.get('device')
    value  = values.get('value')

    if not device or not value: return

    request = requests.get(self.api + self.temp.format(device=device, value=value))
    if request.status_code != requests.codes.ok: return
    self.work.set()
