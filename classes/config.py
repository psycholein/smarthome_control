import yaml

class Config:

  def __init__(self):
    self.base = yaml.load(file('config/base.yml', 'r'))
    self.devices = yaml.load(file('config/devices.yml', 'r'))

  def getWebserverPort(self):
    return self.base.get('webserver')

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

  def initDevices(self, fhem, values):
    climates = self.getClimates()
    for climate in climates:
      values.addCollection(climate.get('clima'), climate.get('room'), 'climate')
      if climate.get('heat'):
        heat = climate.get('heat')+'_Clima'
        values.addCollection(heat, climate.get('room'), 'climate')
        fhem.addDevice(heat, self.getClimateValues())

    energies = self.getEnergies()
    for energy in energies:
      device = energy.get('device')
      values.addCollection(device, energy.get('name'), 'energy')
      fhem.addDevice(device, self.getEnergyValues())

    plants = self.getPlants()
    for plant in plants:
      device = plant.get('device')
      values.addCollection(device, plant.get('room'), 'plant')
