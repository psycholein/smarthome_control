import threading, thread, time, sqlite3, copy

class Logger(threading.Thread):
  types = ['humidity', 'temperature', 'desired-temp']

  def __init__(self, values):
    super(self.__class__, self).__init__()
    self.values  = values
    self.work    = threading.Event()
    self.running = False
    self.logs    = 0

  def run(self):
    self.running = True
    while self.log():
      self.work.wait(300)

  def log(self):
    if self.logs > 0:
      conn = sqlite3.connect('logger.db')
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS logger (
                     uid text, category text, collection text, typ text,
                     value text, timestamp text)''')
      conn.commit()
      self.addLogs(c, conn)
      conn.close()

    self.logs += 1
    return self.running

  def stop(self):
    self.running = False
    self.work.set()

  def addLogs(self, c, conn):
    timestamp = time.time()
    data = copy.deepcopy(self.values.getValues())
    for category, collections in data.iteritems():
      for collection, typs in collections.iteritems():
        for typ, values in typs.iteritems():
          value = values.get('value')
          uid   = values.get('uid')
          if not uid or not value: continue
          if not uid in self.types: continue

          log = (uid, category, collection, typ, value, timestamp)
          c.execute('INSERT INTO logger VALUES (?,?,?,?,?,?)', log)
          conn.commit()
