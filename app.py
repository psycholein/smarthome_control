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
from classes.highcharts import Highcharts
from classes.switch import Switch

class App:

  pidfile = "/tmp/smarthome.pid"

  def __init__(self):
    print "starting smarthome..."
    self.setPid()
    self.threads = []

    self.dispatcher = Dispatcher()
    self.config = Config(self.dispatcher)
    self.values = Values()

    self.hue = Hue(self.config.getHueIP(), self.dispatcher)
    self.hue.start()
    self.threads.append(self.hue)

    self.switch = Switch(self.dispatcher, self.config.getSwitchConfig())

    self.pilight = PilightClient(self.dispatcher)
    self.pilight.registerCallback(self.switch.callback, 'protocol', ['arctech_screen'])
    self.pilight.registerCallback(self.climateCallback, 'protocol', ['alecto_ws1700'])
    self.pilight.start()
    self.threads.append(self.pilight)


    if self.config.hasLCD():
      self.lcd = Lcd(self.values)
      self.lcd.start()
      self.threads.append(self.lcd)

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

    self.highcharts = Highcharts(self.logger, self.dispatcher)

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
        'values': {
          'type': 'values',
          'data': self.values.getValues()
        }
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

def main():
  App()

if __name__ == "__main__":
    main()
