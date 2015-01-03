class Cronjobs:
  cronjobs = []

  def addCronjob(self, command, time):
    Cronjobs.cronjobs.append({
        'command': command,
        'time': time,
        'status': None
      })
    pass

  def checkCronjobs(self):
    pass
