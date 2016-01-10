import time

class Values:
  data        = {}
  collections = {}
  changed     = True

  @staticmethod
  def addValue(uid, typ, value):
    if not Values.collections.has_key(uid): return
    collection = Values.collections.get(uid)
    if not Values.data.get(collection):
      Values.data[collection] = {'collection': collection}
    if Values.data[collection].get(typ) != value:
      Values.changed = True
      Values.data[collection][typ] = {
        'value': value,
        'date':  time.strftime('%X')
      }

  @staticmethod
  def addCollection(uid, name):
    if uid: Values.collections[uid] = name

  @staticmethod
  def getValues():
    return Values.data
