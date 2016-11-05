import time

class Values:
  def __init__(self):
    self.reset()

  def addValue(self, uid, typ, value):
    collection = self.collections.get(str(uid))
    if not collection: return
    data = self.data[collection['category']][collection['name']]
    if not data.get(typ): data[typ] = {}

    updated = data[typ].get('updated')
    if data[typ].get('value') != value:
      self.changed = True
      updated = time.strftime('%X')
    data[typ] = { 'value': value, 'date': time.strftime('%X'),
                  'uid': uid, 'updated': updated }

  def addCollection(self, uid, name, category):
    self.collections[str(uid)] = { 'name': name, 'category': category }
    if not self.data.has_key(category): self.data[category] = {}
    if not self.data[category].has_key(name):
      self.data[category][name] = { 'collection': self.collections[str(uid)] }

  def getValues(self, category = None):
    if not category: return self.data
    return self.data.get(category, {})

  def getValuesCategoryAndRoom(self, category, room):
    return self.data.get(category, {}).get(room)

  def reset(self):
    self.data        = {}
    self.collections = {}
    self.changed     = True
