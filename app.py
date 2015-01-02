import time
from libs.pilight import PilightClient
from libs.hue import Hue
from libs.webserver import Webserver
from classes.output import Output

class App:

  def __init__(self):
    self.hue = Hue('192.168.0.206')
    self.hue.start()

    self.pilight = PilightClient()
    self.pilight.registerCallback(self.switchCallback)
    self.pilight.registerCallback(self.climateCallback, 'protocol', ['threechan'])
    self.pilight.start()

    self.output = Output()
    self.output.addRoom(1433, 'Arbeitszimmer')
    self.output.addRoom(1463, 'Schlafzimmer')
    self.output.addRoom(1324, 'Kinderzimmer')
    self.output.addRoom(1351, 'Badezimmer')
    self.output.addRoom(1453, 'Wohnzimmer')
    self.output.addRoom(1354, 'Kueche')

    self.webserver = Webserver(self.output)
    self.webserver.start()
    self.serve()

  def serve(self):
    print "started!\n"
    threads = [self.hue, self.pilight]
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
        self.pilight.stop()
        self.hue.stop()

  def climateCallback(self, data):
    code = data.get('code', None)
    if not code: return

    temp = float(code.get('temperature')) / 10
    humi = float(code.get('humidity')) / 10
    self.output.addClimate(code.get('id'), temp, humi)

  def switchCallback(self, data):
    code = data.get('code', None)
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
