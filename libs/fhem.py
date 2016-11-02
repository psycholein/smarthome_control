import threading, requests, time

from classes.values import Values

class Fhem(threading.Thread):

  prefix = "/fhem"
  json   = "?cmd=jsonlist2&XHR=1"
  temp   = "?dev.{device}={device}&arg.{device}=desired-temp&val.{device}={value}&cmd.{device}=set&XHR=1"
  energy = "?cmd.{device}=set%20{device}%20{value}&XHR=1"

  def __init__(self, ip, port, dispatcher = None):
    threading.Thread.__init__(self)
    self.api        = "http://%s:%s%s" % (ip, port, self.prefix)
    self.last       = 0
    self.dispatcher = dispatcher
    self.devices    = []
    self.callbacks  = []
    self.work       = threading.Event()
    self.dispatcher.addRoute("setDesiredTemp", self.setDesiredTemp)
    self.dispatcher.addRoute("setEnergy", self.setEnergy)
    self.dispatcher.addRoute("fhem", self.trigger)

  def run(self):
    self.running = True
    while self.getData():
      self.work.wait(60)

  def stop(self):
    self.running = False
    self.work.set()

  def trigger(self, values):
    now = time.time()
    if now <= self.last: return
    print "Fhem trigger"
    self.last = now + 1
    self.work.set()

  def addDevice(self, name, values):
    if name and values: self.devices.append({'name': name, 'values': values})

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

  def isDevice(self, name):
    for device in self.devices:
      if name == device.get('name'): return device
    return None

  def analyzeResults(self, results):
    for result in results.get('Results', []):
      name = result.get('Name')
      device = self.isDevice(name)
      if device:
        data     = {'id': name, 'values': device.get('values')}
        readings = result.get('Readings')
        if not readings: continue
        for attr in device.get('values').get('attr'):
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

  def setEnergy(self, values):
    device = values.get('device')
    value  = values.get('value')
    if not device or not value: return

    request = requests.get(self.api + self.energy.format(device=device, value=value))
    if request.status_code != requests.codes.ok: return
    self.work.set()
