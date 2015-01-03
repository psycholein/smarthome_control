import tornado.ioloop
import tornado.web
import tornado.websocket
import threading, os

class IndexHandler(tornado.web.RequestHandler):
  def initialize(self, output):
    self.output = output

  @tornado.web.asynchronous
  def get(self):
    self.render('index.html', output=self.output)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
  def initialize(self, clients, dispatcher):
    self.clients    = clients
    self.dispatcher = dispatcher

  def open(self, *args):
    self.clients.add(self)
    if self.dispatcher: self.dispatcher.clientConnected(self)
    self.stream.set_nodelay(True)

  def on_message(self, message):
    self.dispatcher.send(message, self)

  def on_close(self):
    self.clients.remove(self)
    if self.dispatcher: self.dispatcher.clientDisconnected(self)


class Clients:
  def __init__(self):
    self.clients = []

  def add(self, client):
    self.clients.append(client)

  def remove(self, client):
    self.clients.remove(client)

  def get(self):
    return self.clients

  def clear(self):
    self.clients = []


class Webserver(threading.Thread):
  def __init__(self, output = None, dispatcher = None):
    super(self.__class__, self).__init__()

    static_path     = os.path.dirname(__file__)+'/../web/static'
    template_path   = os.path.dirname(__file__)+'/../web/views'

    self.dispatcher = dispatcher
    self.clients    = Clients()
    self.running    = False
    self.app        = tornado.web.Application([
      (r'/ws', WebSocketHandler, {
                  "clients"       : self.clients,
                  "dispatcher"    : self.dispatcher
               }),
      (r'/', IndexHandler, {"output": output}),
    ],
    static_path   = static_path,
    template_path = template_path,
    autoreload    = False)

  def run(self):
    self.running = True
    self.app.listen(3000)
    tornado.ioloop.IOLoop.instance().start()

    self.running = False
    self.clients.clear()

  def stop(self):
    if not self.running: return

    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(lambda x: x.stop(), ioloop)
    self.join()

  def send(self, data):
    if not self.running: return

    for client in self.clients.get():
      client.write_message(data)

  def is_running(self):
    return self.running
