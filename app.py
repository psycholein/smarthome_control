import time
from libs.pilight import PilightClient
from libs.hue import Hue
from libs.webserver import Webserver

class App:

  def __init__(self):
    self.hue = Hue('192.168.0.206')
    self.hue.start()
    self.pilight = PilightClient()
    self.pilight.registerCallback(self.callback)
    self.pilight.start()

    self.webserver = Webserver()
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

  def callback(self, data):
    code = data.get('code', None)
    if not code: return

    # TODO config

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


    # Schlafzimmer
    if code.get('id', -1) == 13205286 or code.get('id', -1) == 13205202:
      if code.get('all', -1) == 1:
        self.hue.do({'light': [4], 'cmd': 'on', 'val': False})
      if code.get('unit', -1) == 0:
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 4, 'cmd': 'bri', 'val': 1})
          self.hue.do({'light': 4, 'cmd': 'on', 'val': True})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': 4, 'cmd': 'bri', 'val': 75})
          self.hue.do({'light': 4, 'cmd': 'on', 'val': True})
      if code.get('unit', -1) == 1:
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 4, 'cmd': 'bri', 'val': 150})
          self.hue.do({'light': 4, 'cmd': 'on', 'val': True})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': 4, 'cmd': 'bri', 'val': 255})
          self.hue.do({'light': 4, 'cmd': 'on', 'val': True})
      if code.get('unit', -1) == 2:
        if code.get('state', '') == 'up' :
          self.hue.do({'light': 4, 'cmd': 'xy', 'val': self.hue.RGB2CIE(0,255,0)})
        if code.get('state', '') == 'down' :
          self.hue.do({'light': 4, 'cmd': 'xy', 'val': self.hue.RGB2CIE(255,255,255)})

def main():
  App()

if __name__ == "__main__":
    main()
