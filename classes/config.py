import yaml
from classes.routes import Routes

class Config:

  def __init__(self):
    self.base = yaml.load(file('config/base.yml', 'r'))
    self.devices = yaml.load(file('config/devices.yml', 'r'))

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

  def getPlants(self):
    return self.devices.get('plant').get('devices')

  def getNotification(self):
    return self.base.get('notification')

  def initDevices(self, fhem, values):
    climates = self.getClimates()
    for climate in climates:
      values.addCollection(climate.get('clima'), climate.get('room'))
      values.addValue(climate.get('clima'), 'type', 'climate')
      if climate.get('heat'):
        heat = climate.get('heat')+'_Clima'
        values.addCollection(heat, climate.get('room'))
        values.addValue(heat, 'type', 'climate')
        fhem.addDevice(heat, self.getClimateValues())

    energies = self.getEnergies()
    for energy in energies:
      device = energy.get('device')
      values.addCollection(device, energy.get('name'))
      values.addValue(device, 'type', 'energy')
      fhem.addDevice(device, self.getEnergyValues())

    plants = self.getPlants()
    for plant in plants:
      device = plant.get('device')
      values.addCollection(device, plant.get('room'))
      values.addValue(device, 'type', 'plant')


  def routes(self):
    routes = Routes()
    routes.addRoute('setDesiredTemp', 'Fhem', 'setDesiredTemp')
    routes.addRoute('setEnergy', 'Fhem', 'setEnergy')
    routes.addRoute('outputToJs', 'Webserver', 'send')
    routes.addRoute('hue', 'Hue', 'do')
    routes.addRoute('sensor', 'Api', 'sensor')
    routes.addRoute('notification', 'Notification', 'addClient')
    return routes
