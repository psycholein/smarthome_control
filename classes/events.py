import threading, thread, datetime, time

class Events(threading.Thread):
  def __init__(self, values, dispatcher):
    super(self.__class__, self).__init__()
    self.values     = values
    self.dispatcher = dispatcher
    self.running    = False
    self.events     = []
    self.work       = threading.Event()
    self.time       = 0
    self.week       = []

  def addEvent(self, typ, data):
    self.events.append({
        'typ':     typ,
        'data':    data,
        'status':  {}
      })

  def run(self):
    self.running = True
    while self.check():
      self.work.wait(30)

  def defineValues(self):
    time = datetime.datetime.today()
    self.time = float("%d.%d" % (time.hour, time.minute))
    self.week = ['Mo-So']
    if time.weekday() < 5:
      self.week.append('Mo-Fr')
    else:
      self.week.append('Sa-So')

  def check(self):
    self.defineValues()
    for event in self.events:
      if not self.running: return self.running
      if event['typ'] == 'climate': self.checkClimate(event)
      if event['typ'] == 'energy': self.checkEnergy(event)
    self.work.clear()
    return self.running

  def checkClimate(self, event):
    data = event['data']
    if not data.get('week') in self.week: return
    f = float(data.get('from'))
    t = float(data.get('to'))
    if f < t:
      if self.time < f or self.time >= t: return
    else:
      if self.time < f and self.time >= t: return

    if event['status'].get('done', 0) > time.strftime("%Y-%m-%d %H.%m"): return
    done = True
    for room in data.get('room', []):
      if not self.setTemperature(room, data.get('temperature')): done = False
    if done:
      if f < t:
        event['status']['done'] = time.strftime("%Y-%m-%d ") + data.get('to')
      else:
        temp = time.localtime()
        today = datetime.date(temp.tm_year, temp.tm_mon, temp.tm_mday)
        done = today + datetime.timedelta(days = 1) + ' ' + data.get('to')
        event['status']['done'] = done

  def checkEnergy(self, event):
    pass

  def setTemperature(self, room, temperature):
    if not room or not temperature: return False
    value = self.values.getValuesCategoryAndRoom('climate', room)
    if not value.get('device') or not value.get('desired-temp'): return False
    if float(value.get('desired-temp', {}).get('value')) == float(temperature):
      return True
    data = { "path": "setDesiredTemp",
             "values": {
               "device": value.get('device', {}).get('value'),
               "value": temperature
              } }
    self.dispatcher.send(data)
    return True

  def stop(self):
    self.running = False
    self.work.set()

  def trigger(self, typ, values):
    pass
