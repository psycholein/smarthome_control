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

  def addCollection(self, uid, category, name):
    self.collections[uid] = { 'name': name, 'category': category }
    if not self.data.has_key(category): self.data[category] = {}
    self.data[category][name] = { 'collection': self.collections[uid] }
    self.data[category] = sorted(self.data[category])


  def getValues(self, category):
    return self.data.get(category, {})
