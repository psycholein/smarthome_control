from phue import Bridge
import time

bridge = Bridge('192.168.0.206')
bridge.connect()
bridge.get_api()
bridge.get_light(3, 'on')
time.sleep(5)
bridge.set_light(3, 'bri', 127)
print bridge.get_light(3, 'name')

