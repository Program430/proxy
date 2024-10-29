import json
import socket
import time

sock = socket.socket()
sock.connect(('localhost', 9999))

def send_request_through_proxy(data):
    sock.send(data)
    data = sock.recv(1024)
    original_data = json.loads(data)
    print(original_data)

json_data = {
   "name": "Apple MacBook Pro 1555",
   "data": {
      "year": 2019,
      "price": 1849.99,
      "CPU model": "Intelll Core i19",
      "Hard disk size": "15 TB"
   }
}

with sock:
    while True:
        time.sleep(0.5)
        data = {
            'url':'https://api.restful-api.dev/objects',
            'headers': {
                'Content-Type': 'application/json'
            },
            'json': json_data,
        }
        data = json.dumps(data)
        data = data.encode()
        send_request_through_proxy(data)


