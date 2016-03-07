import time

class Values:
  def __init__(self):
    self.data        = {}
    self.collections = {}
    self.changed     = True

  def addValue(self, uid, typ, value):
    if not self.collections.has_key(uid): return
    collection = self.collections.get(uid)
    if not self.data.get(collection):
      self.data[collection] = {'collection': collection}
    if self.data[collection].get(typ) != value:
      self.changed = True
      self.data[collection][typ] = {
        'value': value,
        'date':  time.strftime('%X')
      }

  def addCollection(self, uid, name):
    if uid: self.collections[uid] = name

  def getValues(self):
    return self.data

  def getCollectionValues(self, collection):
    return self.data.get(collection, {})
