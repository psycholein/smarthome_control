import time

class Values:
  def __init__(self):
    self.data        = {}
    self.collections = {}
    self.changed     = True

  def addValue(self, uid, typ, value):
    collection = self.collections.get(uid)
    if not collection: return
    data = self.data[collection['category']][collection['name']].get(str(typ))
    if not data:
      self.data[collection['category']][collection['name']][str(typ)] = {}
      data = self.data[collection['category']][collection['name']][str(typ)]
    if data[str(typ)].get('value') != value:
      self.changed = True
      data[str(typ)] = { 'value': value, 'date': time.strftime('%X') }

  def addCollection(self, uid, catgeory, name):
    self.collections[uid] = {'name': name, 'catgeory': catgeory}
    if not self.data.has_key(catgeory): self.data[catgeory] = {}
    self.data[catgeory][name] = { 'collection': self.collections[uid] }
    self.data[catgeory] = sorted(self.data[catgeory])


  def getValues(self, catgeory):
    return self.data.get(category, {})
