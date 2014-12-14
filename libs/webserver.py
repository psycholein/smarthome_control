from flask import Flask
from multiprocessing import Process
app = Flask(__name__)

class Webserver:

  def __init__(self):
    global app
    self.server = Process(target=app.run, args=('0.0.0.0', 3000,))

  @app.route("/")
  def hello(self):
    return "Hello World!"

  def start(self):
    self.server.start()

  def stop(self):
    self.server.terminate()
    self.server.join()
