class Output:
  def __init__(self):
    self.climate = {}
    self.rooms   = {}

  def addClimate(self, uid, temperature, humidity):
    if not self.rooms.has_key(uid): return
    self.climate[uid] = {
      'temperature': temperature,
      'humidity':    humidity,
      'room':        self.rooms.get(uid)
    }

  def addRoom(self, uid, name):
    self.rooms[uid] = name

  def getValues(self):
    return self.climate
