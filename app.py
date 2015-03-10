import time, json, os, sys, signal
from libs.pilight import PilightClient
from libs.hue import Hue
from libs.fhem import Fhem
from classes.config import Config
from classes.webserver import Webserver
from classes.values import Values
from classes.dispatcher import Dispatcher
from classes.events import Events

class App:

  pidfile = "/tmp/smarthome.pid"

  def __init__(self):
    print "starting smarthome..."
    self.setPid()

    self.config = Config()
    self.dispatcher = Dispatcher(self.config.routes())

    self.hue = Hue(self.config.getHueIP(), self.dispatcher)
    self.hue.start()

    self.pilight = PilightClient(self.dispatcher)
    self.pilight.registerCallback(self.switchCallback)
    self.pilight.registerCallback(self.climateCallback, 'protocol', ['threechan'])
    self.pilight.start()

    self.fhem = Fhem(self.config.getFhemIp(), self.config.getFhemPort(), self.dispatcher)
    for attr in self.config.fhemAttr(): self.fhem.addAttribute(attr)
    self.fhem.registerCallback(self.fhemCallback)

    sensors = self.config.getSensors()
    for room in sensors:
      sensor = sensors[room]
      Values.addRoom(sensor.get('clima'), room)
      if sensor.get('heat'):
        heat = sensor.get('heat')+'_Clima'
        Values.addRoom(heat, room)
        self.fhem.addDevice(heat)

    self.fhem.start()

    self.events = Events(self.dispatcher)
    self.events.start()

    self.webserver = Webserver(self.dispatcher)
    self.webserver.start()

    self.dispatcher.addDispatchObject(self)
    self.dispatcher.addDispatchObject(self.hue)
    self.dispatcher.addDispatchObject(self.pilight)
    self.dispatcher.addDispatchObject(self.fhem)
    self.dispatcher.addDispatchObject(self.events)
    self.dispatcher.addDispatchObject(self.webserver)
    self.dispatcher.start()

    self.serve()

    self.clearPid()

  def setPid(self):
    pid = str(os.getpid())
    if os.path.isfile(self.pidfile):
      try:
        os.kill(int(file(self.pidfile,'r').readlines()[0]), 15)
      except:
        pass
      else:
        time.sleep(5)
    file(self.pidfile, 'w').write(pid)

  def clearPid(self):
    os.unlink(self.pidfile)

  def serve(self):
    print "started!\n"
    threads = [self.hue, self.pilight, self.fhem, self.events, self.dispatcher]
    while True:
      try:
        run = False
        for thread in threads:
          thread.join(1)
          if thread.isAlive(): run = True
        if not run:
          self.webserver.stop()
          return
      except KeyboardInterrupt:
        for thread in threads: thread.stop()
      finally:
        if Values.changed:
          data = {
            'params': ['path', 'values'],
            'path':   'outputToJs',
            'values': Values.getValues()
          }
          Values.changed = False
          self.dispatcher.send(data)

  def fhemCallback(self, data):
    print data
    uid = data.get('id')
    for attr in self.config.fhemAttr():
      value = data.get(attr)
      if value:
        if attr == 'state':
          if value.find('set_desired-temp') != -1:
            desired = value.replace('set_desired-temp','').strip()
            Values.addValue(uid, 'desired-temp', desired)
            Values.addValue(uid, 'info', 'Set to %s&deg;C (Current: %s&deg;C)' %(desired, data.get('desired-temp')))
          else:
            Values.addValue(uid, 'info', '')
        else:
          Values.addValue(uid, attr, value)
          Values.addValue(uid, 'device', uid)

  def climateCallback(self, data):
    code = data.get('code')
    if not code: return

    temperature = float(code.get('temperature')) / 10
    humidity    = float(code.get('humidity')) / 10

    Values.addValue(code.get('id'), 'temperature', temperature)
    Values.addValue(code.get('id'), 'humidity', humidity)

  def switchCallback(self, data):
    code = data.get('code')
    if not code: return

    # TODO config
    # Wohnzimmer Lichtschalter
    if code.get('id', -1) == 13583562:
      if code.get('unit', -1) == 10:
        if code.get('state', '') == 'down':
          self.hue.do({'light': 3, 'cmd': 'on', 'val': False})
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 3, 'cmd': 'on', 'val': True})
          self.hue.do({'light': 3, 'cmd': 'bri', 'val': 255})
      if code.get('unit', -1) == 11:
        self.hue.do({'light': 3, 'cmd': 'on', 'val': True})
        if code.get('state', '') == 'down':
          self.hue.do({'light': 3, 'cmd': 'bri', 'val': 32})
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 3, 'cmd': 'bri', 'val': 127})

    # Wohnzimmer Fernbedienung
    if code.get('id', -1) == 13184550:
      if code.get('all', -1) == 1:
        self.hue.do({'light': [1,2,3,5], 'cmd': 'on', 'val': False})
      if code.get('unit', -1) == 0:
        if code.get('state', '') == 'up' :
          self.hue.do({'light': [1,2], 'cmd': 'on', 'val': True})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': [1,2], 'cmd': 'on', 'val': False})
      if code.get('unit', -1) == 1:
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 3, 'cmd': 'on', 'val': True})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': 3, 'cmd': 'on', 'val': False})
      if code.get('unit', -1) == 2:
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 5, 'cmd': 'on', 'val': True})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': 5, 'cmd': 'on', 'val': False})


    # Schlafzimmer 2 Fernbedienungen
    if code.get('id', -1) == 13205286 or code.get('id', -1) == 13205202:
      if code.get('all', -1) == 1:
        self.hue.do({'light': [4], 'cmd': 'on', 'val': False})
      if code.get('unit', -1) == 0:
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 4, 'cmd': 'on', 'val': True})
          self.hue.do({'light': 4, 'cmd': 'bri', 'val': 1})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': 4, 'cmd': 'on', 'val': True})
          self.hue.do({'light': 4, 'cmd': 'bri', 'val': 75})
      if code.get('unit', -1) == 1:
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 4, 'cmd': 'on', 'val': True})
          self.hue.do({'light': 4, 'cmd': 'bri', 'val': 150})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': 4, 'cmd': 'on', 'val': True})
          self.hue.do({'light': 4, 'cmd': 'bri', 'val': 255})
      if code.get('unit', -1) == 2:
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 4, 'cmd': 'xy', 'val': self.hue.RGB2CIE(0,255,0)})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': 4, 'cmd': 'xy', 'val': self.hue.RGB2CIE(255,255,0)})

def main():
  App()

if __name__ == "__main__":
    main()
