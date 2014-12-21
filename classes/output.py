class Output:
  def __init__(self):
    self.climate = {}
    self.rooms   = {}

  def addClimate(self, uid, temperature, humidity):
    if not self.rooms.has_key(uid): return
    room = self.rooms.get(uid)
    self.climate[room] = {
      'temperature': temperature,
      'humidity':    humidity,
      'room':        room
    }

  def addRoom(self, uid, name):
    self.rooms[uid] = name

  def getValues(self):
    return self.climate
