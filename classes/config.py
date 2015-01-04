from classes.routes import Routes

class Config:

  def getHueIP(self):
    return '192.168.0.206'

  def fhemData(self):
    return {
      'ip':   '127.0.0.1',
      'port': '8083'
    }

  def getFhemIp(self):
    return self.fhemData().get('ip')

  def getFhemPort(self):
    return self.fhemData().get('port')

  def getSensors(self):
    return {
      'Arbeitszimmer': {
        'clima': 1433,
        'heat': None
      },
      'Schlafzimmer': {
        'clima': 1463,
        'heat': None
      },
      'Kinderzimmer': {
        'clima': 1324,
        'heat': None
      },
      'Badezimmer': {
        'clima': 1351,
        'heat': None
      },
      'Wohnzimmer': {
        'clima': 1453,
        'heat': None
      },
      'Kueche': {
        'clima': 1354,
        'heat': None
      }
    }

  def routes(self):
    self.routes = Routes()
    # add route
    return self.routes
