class Output:
  climate = {}
  rooms   = {}

  @staticmethod
  def addValue(uid, typ, value):
    if not Output.rooms.has_key(uid): return
    room = Output.rooms.get(uid)
    if not Output.climate.get(room, None): Output.climate[room] = {'room': room}
    Output.climate[room][typ] = value

  @staticmethod
  def addRoom(uid, name):
    Output.rooms[uid] = name

  @staticmethod
  def getValues():
    return Output.climate
