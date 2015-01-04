class Values:
  climate = {}
  rooms   = {}

  @staticmethod
  def addValue(uid, typ, value):
    if not Values.rooms.has_key(uid): return
    room = Values.rooms.get(uid)
    if not Values.climate.get(room, None): Values.climate[room] = {'room': room}
    Values.climate[room][typ] = value

  @staticmethod
  def addRoom(uid, name):
    if uid: Values.rooms[uid] = name

  @staticmethod
  def getValues():
    return Values.climate
