# -*- coding: utf-8 -*-
import threading
import copy
from components.lcddriver import lcd
from classes.values import Values

class Lcd(threading.Thread):

  def __init__(self, values):
    threading.Thread.__init__(self)
    self.work       = threading.Event()
    self.running    = True
    self.values     = values
    self.lcd        = lcd()

  def run(self):
    self.running = True
    while self.running:
      values = copy.deepcopy(self.values.getValues())
      for val in sorted(values):
        self.showData(values.get(val))
        self.work.wait(5)
        if not self.running: return
      self.work.wait(1)

  def showData(self, data):
    if not self.running: return self.running
    self.work.clear()
    self.lcd.lcd_clear()
    self.lcd.lcd_display_string(data.get('collection', ''), 1)
    temp = data.get('temperature',{}).get('value','')
    self.lcd.lcd_display_string("Temperatur: %s" % temp, 2)
    hum = data.get('humidity',{}).get('value','')
    self.lcd.lcd_display_string("Feuchtigkeit: %s" % hum, 3)
    temp = data.get('measured-temp',{}).get('value','')
    temp2 = data.get('desired-temp',{}).get('value','')
    if len(temp) > 0 or len(temp2) > 0:
      self.lcd.lcd_display_string("Heizung: %s / %s" % (temp, temp2), 4)

    return self.running

  def stop(self):
    self.running = False
    self.work.set()
