import yaml
from classes.routes import Routes

class Config:

  def __init__(self):
    self.base = yaml.load(file('config/base.yml', 'r'))
    self.devices = yaml.load(file('config/devices.yml', 'r'))

    print self.devices

  def getHueIP(self):
    return self.base.get('hue')

  def fhemData(self):
    return self.base.get('fhem')

  def getFhemIp(self):
    return self.fhemData().get('ip')

  def getFhemPort(self):
    return self.fhemData().get('port')

  def getClimates(self):
    return self.devices.get('climate').get('devices')

  def getClimateValues(self):
    return {'attr': self.devices.get('climate').get('attr'),
            'type': 'climate', 'config': self.getClimates()}

  def getEnergies(self):
    return self.devices.get('energy').get('devices')

  def getEnergyValues(self):
    return {'attr': self.devices.get('energy').get('attr'),
            'type': 'energy', 'config': self.getEnergies()}


  def routes(self):
    routes = Routes()
    routes.addRoute('setDesiredTemp', 'Fhem', 'setDesiredTemp')
    routes.addRoute('setEnergy', 'Fhem', 'setEnergy')
    routes.addRoute('outputToJs', 'Webserver', 'send')
    return routes
