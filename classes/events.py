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
    self.last       = 0
    self.week       = []
    self.dispatcher.addRoute("events", self.trigger)

  def addEvent(self, typ, data):
    self.events.append({
        'typ':     typ,
        'data':    data,
        'status':  {}
      })

  def trigger(self, values = None):
    now = time.time()
    if now <= self.last: return
    self.last = now + 1
    self.work.set()

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
    if not self.checkTime(data): return
    if event['status'].get('done', 0) > time.strftime("%Y-%m-%d %H.%m"): return
    done = True
    for room in data.get('room', []):
      if not self.setTemperature(room, data.get('temperature')): done = False
    if done:
      if float(data.get('from')) < float(data.get('to')):
        event['status']['done'] = time.strftime("%Y-%m-%d ") + data.get('to')
      else:
        temp = time.localtime()
        today = datetime.date(temp.tm_year, temp.tm_mon, temp.tm_mday)
        done = (today + datetime.timedelta(days = 1)) + ' ' + data.get('to')
        event['status']['done'] = done

  def checkEnergy(self, event):
    data = event['data']
    if not self.checkTime(data):
      if event['status'].get('on'):
        event['status']['on'] = False
        self.setEnergy(data.get('name'), 'off')
      return
    contact = self.values.getValuesCategoryAndRoom('contact', data.get('room'))
    if contact and contact.get('state', {}).get('value') == 'open':
      self.setTemperature(data.get('room'), data.get('temperature_open'))
      self.setEnergy(data.get('name'), 'off')
      event['status']['on'] = False
      event['status']['opened'] = True
    else:
      self.setTemperature(data.get('room'), data.get('temperature_closed'))
      react = format(datetime.datetime.now() - datetime.timedelta(minutes=data.get('reactivate', 30)), '%H:%M:%S')
      if contact and event['status'].get('opened', False) and contact.get('state', {}).get('updated', 0) > react: return
      event['status']['opened'] = False
      humidity = self.values.getValuesCategoryAndRoom('climate', data.get('room'))
      if not humidity: return
      hum = float(humidity.get('humidity', {}).get('value', 0))
      if hum >= float(data.get('humidity_start')):
        if event['status'].get('on'): return
        self.setEnergy(data.get('name'), 'on')
        event['status']['on'] = True
      elif event['status'].get('on') and hum <= float(data.get('humidity_end')):
        self.setEnergy(data.get('name'), 'off')
        event['status']['on'] = False

  def checkTime(self, data):
    if not data.get('week') in self.week: return False
    f = float(data.get('from'))
    t = float(data.get('to'))
    if f < t:
      if self.time < f or self.time >= t: return False
    else:
      if self.time < f and self.time >= t: return False
    return True

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

  def setEnergy(self, room, state):
    if not room or not state: return False
    value = self.values.getValuesCategoryAndRoom('energy', room)
    if not value.get('device') or not value.get('state'): return False
    if value.get('state', {}).get('value') == state: return True
    data = { "path": "setEnergy",
             "values": {
               "device": value.get('device', {}).get('value'),
               "value": state
              } }
    self.dispatcher.send(data)
    return True

  def stop(self):
    self.running = False
    self.work.set()
