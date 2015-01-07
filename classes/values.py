class Values:
  climate = {}
  rooms   = {}
  changed = True

  @staticmethod
  def addValue(uid, typ, value):
    if not Values.rooms.has_key(uid): return
    room = Values.rooms.get(uid)
    if not Values.climate.get(room, None): Values.climate[room] = {'room': room}
    if Values.climate[room].get(typ, None) != value:
      Values.changed = True
      Values.climate[room][typ] = value

  @staticmethod
  def addRoom(uid, name):
    if uid: Values.rooms[uid] = name

  @staticmethod
  def getValues():
    return Values.climate
