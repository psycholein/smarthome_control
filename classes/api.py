class Api:
  def __init__(self, values, dispatcher):
    self.values = values
    self.dispatcher = dispatcher
    self.dispatcher.addRoute("sensor", self.sensor)

  def sensor(self, values):
    device = values.get('device')
    value  = values.get('value')
    if not device or not value: return

    self.values.addValue(device, 'humidity', value)
    self.values.addValue(device, 'device', device)
