import threading, thread, time, sqlite3, copy

class Logger(threading.Thread):
  types = ['humidity', 'temperature', 'measured-temp', 'desired-temp', 'state']

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

  def dict_factory(self, cursor, row):
      d = {}
      for idx,col in enumerate(cursor.description):
          d[col[0]] = row[idx]
      return d

  def db(self):
    conn = sqlite3.connect('logger.db')
    conn.row_factory = self.dict_factory
    return conn

  def log(self):
    if self.logs > 0 and self.running:
      conn = self.db()
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS logger (
                     uid text, category text, collection text, typ text,
                     value text, timestamp text)''')
      c.execute('''CREATE INDEX IF NOT EXISTS search_without_typ ON logger
                     (category, collection, timestamp)''')
      c.execute('''CREATE INDEX IF NOT EXISTS search_with_typ ON logger
                     (category, collection, timestamp, typ)''')
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
          if typ not in self.types: continue

          log = (uid, category, collection, typ, value, timestamp,)
          c.execute('INSERT INTO logger VALUES (?,?,?,?,?,?)', log)
          conn.commit()

  def readLogs(self, category, collection, typ = None, since = None):
    if not since: since = time.time() - 3600 * 24
    conn = self.db()
    c = conn.cursor()
    if not typ:
      query = (since, category, collection,)
      c.execute('''SELECT * FROM logger
                     WHERE timestamp>=? and category=? and collection=?
                     ORDER BY CAST(timestamp AS INTEGER) ASC''', query)
    else:
      query = (since, category, collection, typ,)
      c.execute('''SELECT * FROM logger
                     WHERE timestamp>=? and category=? and collection=? and
                     typ=? ORDER BY CAST(timestamp AS INTEGER) ASC''', query)
    return c.fetchall()
