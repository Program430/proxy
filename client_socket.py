import json
import socket
import time

class RequestThroughProxy:
    def __init__(self, url, headers):
        self.sock = socket.socket()
        self.sock.connect(('localhost', 80))
        self.data = {
            'url': url,
            'headers': headers,
        }

    def send(self, message):
        json_data = {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "model": "llama3-8b-8192"
        }
        self.data['json'] = json_data
        data = json.dumps(self.data)
        data = data.encode()
        return self.__send_request_through_proxy(data)

    def __send_request_through_proxy(self,data):
        self.sock.send(data)
        data = self.sock.recv(1024)
        original_data = json.loads(data)
        return original_data

url = ''

headers = {
    'Content-Type': 'application/json',
    "Authorization": "Bearer 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",
}

message = "Что такое энергия"

request_1 = RequestThroughProxy(url, headers, message)

print(request_1.send())

