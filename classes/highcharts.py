class Highcharts:
  def __init__(self, logger, dispatcher):
    self.logger = logger
    self.dispatcher = dispatcher
    self.dispatcher.addRoute("highchart", self.data)

  def data(self, values):
    category   = values.get('category')
    collection = values.get('collection')
    typ        = values.get('typ')
    since      = values.get('since')
    if not category or not collection: return

    logs = self.logger.readLogs(category, collection, typ, since)
    data = {
      'params': ['path', 'values'],
      'path':   'outputToJs',
      'values': {
        'type': 'highchart',
        'data': logs
      }
    }
    self.dispatcher.send(data)
