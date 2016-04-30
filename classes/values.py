import time

class Values:
  def __init__(self):
    self.data        = {}
    self.collections = {}
    self.changed     = True

  def addValue(self, uid, typ, value):
    collection = self.collections.get(str(uid))
    if not collection: return
    data = self.data[collection['category']][collection['name']]
    if not data.get(typ): data[typ] = {}
    if data[typ].get('value') != value: self.changed = True
    data[typ] = { 'value': value, 'date': time.strftime('%X') }

  def addCollection(self, uid, name, category):
    self.collections[str(uid)] = { 'name': name, 'category': category }
    if not self.data.has_key(category): self.data[category] = {}
    if not self.data[category].has_key(name):
      self.data[category][name] = { 'collection': self.collections[str(uid)] }

  def getValues(self, category = None):
    if not category: return self.data
    return self.data.get(category, {})
