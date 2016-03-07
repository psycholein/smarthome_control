class Api:
  def sensor(self, values):
    device = values.get('device')
    value  = values.get('value')
    print device, value, values, "\n\n"
    if not device or not value: return

    self.values.addValue(device, 'humidity', value)
    self.values.addValue(device, 'device', device)
