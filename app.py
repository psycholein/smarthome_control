import time, json, os, sys, signal
from libs.pilight import PilightClient
from libs.hue import Hue
from libs.fhem import Fhem
from libs.lcd import Lcd
from classes.config import Config
from classes.webserver import Webserver
from classes.values import Values
from classes.dispatcher import Dispatcher
from classes.events import Events
from classes.api import Api
from classes.logger import Logger

class App:

  pidfile = "/tmp/smarthome.pid"

  def __init__(self):
    print "starting smarthome..."
    self.setPid()
    self.threads = []

    self.config = Config()
    self.values = Values()
    self.dispatcher = Dispatcher()

    self.hue = Hue(self.config.getHueIP(), self.dispatcher)
    self.hue.start()
    self.threads.append(self.hue)

    self.pilight = PilightClient(self.dispatcher)
    self.pilight.registerCallback(self.switchCallback, 'protocol', ['arctech_screen'])
    self.pilight.registerCallback(self.climateCallback, 'protocol', ['alecto_ws1700'])
    self.pilight.start()
    self.threads.append(self.pilight)

    #self.lcd = Lcd(self.values)
    #self.lcd.start()
    #self.threads.append(self.lcd)

    self.fhem = Fhem(self.config.getFhemIp(), self.config.getFhemPort(), self.dispatcher)
    self.fhem.registerCallback(self.fhemCallback)
    self.config.initDevices(self.fhem, self.values)
    self.fhem.start()
    self.threads.append(self.fhem)

    self.api = Api(self.values, self.dispatcher)

    self.events = Events(self.dispatcher)
    self.events.start()
    self.threads.append(self.events)

    self.logger = Logger(self.values)
    self.logger.start()
    self.threads.append(self.logger)

    self.webserver = Webserver(self.values, self.dispatcher, self.config.getWebserverPort())
    self.webserver.start()

    self.dispatcher.start()
    self.threads.append(self.dispatcher)
    self.serve()

    self.clearPid()

  def setPid(self):
    pid = str(os.getpid())
    if os.path.isfile(self.pidfile):
      try:
        os.kill(int(file(self.pidfile,'r').readlines()[0]), 9)
      except:
        pass
      else:
        time.sleep(2)
    file(self.pidfile, 'w').write(pid)

  def clearPid(self):
    os.unlink(self.pidfile)

  def serve(self):
    print "started!\n"
    while True:
      try:
        run = False
        for thread in self.threads:
          self.sendChanges()
          thread.join(1)
          if thread.isAlive(): run = True
        if not run:
          self.webserver.stop()
          for thread in self.threads:
            if thread.isAlive(): thread.stop()
          return
      except KeyboardInterrupt:
        for thread in self.threads: thread.stop()

  def sendChanges(self):
    if self.values.changed:
      data = {
        'params': ['path', 'values'],
        'path':   'outputToJs',
        'values': self.values.getValues()
      }
      self.values.changed = False
      self.dispatcher.send(data)

  def fhemCallback(self, data):
    uid = data.get('id')
    for attr in data.get('values').get('attr'):
      value = data.get(attr)
      if value:
        if attr == 'state' and data.get('values').get('type') == 'climate':
          if value.find('set_desired-temp') != -1:
            desired = value.replace('set_desired-temp','').strip()
            self.values.addValue(uid, 'desired-temp', desired)
            self.values.addValue(uid, 'info', 'Set to %s&deg;C (Current: %s&deg;C)' %(desired, data.get('desired-temp')))
          else:
            self.values.addValue(uid, 'info', '')
        else:
          self.values.addValue(uid, attr, value)
          self.values.addValue(uid, 'device', uid)

  def climateCallback(self, data):
    code = data.get('message')
    if not code: return

    temperature = code.get('temperature')
    humidity    = code.get('humidity')

    if temperature: self.values.addValue(code.get('id'), 'temperature', temperature)
    if humidity: self.values.addValue(code.get('id'), 'humidity', humidity)

  def switchCallback(self, data):
    code = data.get('message')
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
        self.hue.do({'light': [1,2,3,4], 'cmd': 'on', 'val': False})
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
          self.hue.do({'light': 4, 'cmd': 'on', 'val': True})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': 4, 'cmd': 'on', 'val': False})


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
