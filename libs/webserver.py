from flask import Flask
from multiprocessing import Process

class Webserver:

  def __init__(self):
    self.app = Flask(__name__)
    self.server = Process(target=self.app.run)

  @app.route("/")
  def hello(Self):
    return "Hello World!"

  def start(self):
    server.start()

  def stop(self):
    self.server.terminate()
    self.server.join()
