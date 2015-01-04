from classes.routes import Routes

class Config:

  def getHueIP(self):
    return '192.168.0.206'

  def fhemData(self):
    return {
      'ip':   '127.0.0.1',
      'port': '8083'
    }

  def fhemAttr(self):
    return ['desired-temp', 'measured-temp']

  def getFhemIp(self):
    return self.fhemData().get('ip')

  def getFhemPort(self):
    return self.fhemData().get('port')

  def getSensors(self):
    return {
      'Arbeitszimmer': {
        'clima': 1433,
        'heat': 'CUL_HM_HM_CC_RT_DN_319E0E'
      },
      'Schlafzimmer': {
        'clima': 1463,
        'heat': 'CUL_HM_HM_CC_RT_DN_319DFF'
      },
      'Kinderzimmer': {
        'clima': 1324,
        'heat': 'CUL_HM_HM_CC_RT_DN_2E2CBF'
      },
      'Badezimmer': {
        'clima': 1351,
        'heat': None
      },
      'Wohnzimmer': {
        'clima': 1453,
        'heat': 'CUL_HM_HM_CC_RT_DN_319DF0'
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
