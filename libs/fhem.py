import threading

class Fhem(threading.Thread):

  def __init__(self, ip, port):
    threading.Thread.__init__(self)
