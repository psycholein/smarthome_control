class Switch:
  def __init__(self, dispatcher, config):
    self.dispatcher = dispatcher
    self.config = config

  def callback(self, data):
    code = data.get('message')
    if not code: return
    self.analyze(code, self.config)


  def analyze(self, code, config):
    do = None
    cmd = None
    found = False
    for item in config:
      if isinstance(item, dict):
        self.analyze(code, item)
        continue

      if item == 'do':
        do = config[item]
        continue
      if item == 'hue_cmd':
        cmd = { 'hue': config[item] }
        continue
      if str(code.get(item, -1)) == str(config[item]):
        found = True

    if cmd:
      values = cmd.get('hue')
      if values:
        data = {
          'path': 'hue',
          'values': values
        }
        self.dispatcher.send(data)

    if found and do:
      self.analyze(code, do)
