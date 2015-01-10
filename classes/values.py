import time

class Values:
  climate = {}
  rooms   = {}
  changed = True

  @staticmethod
  def addValue(uid, typ, value):
    if not Values.rooms.has_key(uid): return
    room = Values.rooms.get(uid)
    if not Values.climate.get(room): Values.climate[room] = {'room': room}
    if Values.climate[room].get(typ) != value:
      Values.changed = True
      Values.climate[room][typ] = {
        'value': value,
        'date':  time.strftime('%X')
      }

  @staticmethod
  def addRoom(uid, name):
    if uid: Values.rooms[uid] = name

  @staticmethod
  def getValues():
    return Values.climate
