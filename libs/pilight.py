import socket
import httplib
import StringIO
import struct
import re
import threading
import select
import json

class PilightClient(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.callbacks = []
    self.lastData  = {}

  def discover(self, service, timeout=2, retries=1):
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}'.format(*group),
        'MAN: "ssdp:discover"',
        'ST: {st}','MX: 3','',''])

    responses = {}
    i = 0
    for _ in range(retries):
      i += 1
      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', 0, 10000))
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
      sock.sendto(message.format(st=service), group)
      while True:
        try:
          responses[i] = sock.recv(1024)
          break
        except socket.timeout:
          break
        except:
            print "no pilight ssdp connections found"
            break
    return responses.values()

  def registerCallback(self, callback, states = ['up', 'down']):
    self.callbacks.append({'callback': callback, 'states': states})

  def doCallbackIf(self, callback, data):
    if data.get('code', {}).get('state') in callback.get('states', []):
      if data.get('repeats', 0) % 10 == 1:
        self.saveData(data)
        func = callback.get('callback', None)
        if func: func(data)

  def checkCallbacks(self, data):
    for callback in self.callbacks:
      self.doCallbackIf(callback, data)

  def saveData(self, data):
    self.lastData = data

  def decode(self, data):
    try:
      data = json.loads(data)
      print data
    except:
      return
    self.checkCallbacks(data)

  def stop(self):
    self.stopped = True

  def run(self):
    self.stopped = False
    responses = self.discover("urn:schemas-upnp-org:service:pilight:1")
    if len(responses) > 0:
      locationsrc = re.search('Location:([0-9.]+):(.*)', str(responses[0]), re.IGNORECASE)
      if locationsrc:
        location = locationsrc.group(1)
        port = locationsrc.group(2)

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((location, int(port)))
      s.settimeout(None)
      s.send('{"message":"client receiver"}\n')
      data = ""
      while True:
        ready = select.select([s], [], [], 10)
        if not ready[0]: return
        line = s.recv(1024)
        data += line
        if "\n\n" in line[-2:]:
          data = data[:-2]
          break
      if data == '{"message":"accept client"}':
        data = ""
        while True:
          if self.stopped: return
          ready = select.select([s], [], [], 1)
          if not ready[0]: continue
          line = s.recv(1024)
          data += line
          if "\n\n" in line[-2:]:
            data = data[:-2]
            self.decode(data)
            data = ""
      s.close()
      print "socket closed"
