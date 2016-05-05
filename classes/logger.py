import threading, thread, time, sqlite3

class Logger(threading.Thread):
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
      timestamp = time.time()
      conn = sqlite3.connect('logger.db')
      c = conn.cursor()

      c.execute('''CREATE TABLE IF NOT EXISTS logger (
                     uid text, category text, collection text, type text,
                     value text, timestamp text)''')

      conn.close()

    self.logs += 1
    return self.running

  def stop(self):
    self.running = False
    self.work.set()
