import threading
import components.lcddriver
from classes.values import Values

class Lcd(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.work       = threading.Event()
    self.running    = True
    self.lcd        = lcddriver.lcd()

  def run(self):
    self.running = True
    while self.running:
      for data in Values.getValues()
        self.showData(data)
        self.work.wait(10)
        if not self.running: return

  def showData(self, data):
    if not self.running: return self.running
    self.work.clear()
    self.lcd.lcd_clear()
    lcd.lcd_display_string(data.get('room'), 1)
    str = data.get('temperature',{}).get('value','')
    lcd.lcd_display_string("Temperatur: %s°C" % str, 2)
    str = data.get('humidity',{}).get('value','')
    lcd.lcd_display_string("Luftfeuchtigkeit: %s%" % str, 3)
    str = data.get('measured-temp',{}).get('value','')
    str2 = data.get('desired-temp',{}).get('value','')
    if len(str) > 0 or len(str2) > 0:
      lcd.lcd_display_string("Heizung: %s°C / %s°C" % (str, str2), 4)

    return self.running

  def stop(self):
    self.running = False
    self.work.set()
