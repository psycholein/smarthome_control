import threading, thread, datetime

class Events(threading.Thread):
  def __init__(self, dispatcher = None):
    super(self.__class__, self).__init__()
    self.dispatcher = dispatcher
    self.running    = False
    self.events     = []
    self.work       = threading.Event()
    self.time       = 0
    self.week       = []

  def addEvent(self, typ, data):
    self.events.append({
        'typ':     typ,
        'data':   data,
        'status':  None
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
    if not data.week in self.week: return
    if float(data['from']) < self.time or float(data['to']) >= self.time: return
    pass

 def checkEnergy(self, event):
   pass

  def stop(self):
    self.running = False
    self.work.set()

  def trigger(self, typ, values):
    pass
