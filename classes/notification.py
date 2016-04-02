import requests, json

class Notification:
  def __init__(self, key):
    self.key = key
    self.clients = []
    self.url = "https://android.googleapis.com/gcm/send"

  def addClient(self, values):
    client = values.get('client')
    if not client: return

    client = str(client)
    client = client.split('/')
    if len(client) == 0: return

    self.clients.append(client[-1])
    self.push("mal gucken")

  def push(self, message):
    if len(self.clients) == 0: return
    data = {
      'registration_ids': self.clients,
    }
    headers = {
      'Authorization': 'key='+self.key,
      'Content-Type': 'application/json'
    }
    r = requests.post(self.url, headers=headers, data=json.dumps(data))
    print(r.text)
    # TODO: save message text
    # https://android.googleapis.com/gcm/send/fPFOvn5X-50:APA91bH2LKETf2UGqcJwO5mme3h3ma9xD8Tjdk2FYBtMui9AfIhuneQipWR6uMpu5lH0r68ehKUgeNxU-09jBzrMm2vXzlHnZooW0CMdRqknzOF66BpQ0gbTWNXASvOhyEVOZ00SfTWq
