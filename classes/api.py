class Api:
  def sensor(self, values):
    print device, value, "\n\n"
    device = values.get('device')
    value  = values.get('value')
    if not device or not value: return

    self.values.addValue(device, 'humidity', value)
    self.values.addValue(device, 'device', device)
