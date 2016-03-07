class Api:
  def sensor(self, values):
    device = values.get('device')
    value  = values.get('value')
    if not device or not value: return
    print device, value, "\n\n"

    self.values.addValue(device, 'humidity', value)
    self.values.addValue(device, 'device', device)
