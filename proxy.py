import json
import asyncio
import socket
import aiohttp

CONNECT_COUNT = 10

class AsincSocketCloser:
    def __init__(self, sock):
        self.sock = sock

    async def __aenter__(self):
        return self.sock

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


class ProxyResult:
    def __init__(self, data, status) -> None:
        self.data = data
        self.status = status

    def send_data(self):
        data = json.dumps({'data': self.data,
                           'status': self.status})
        
        return data.encode()


class Server:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('', 9999)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen(CONNECT_COUNT)

    @classmethod
    async def __listener(cls):
        while True:
            connection, _ = await asyncio.get_running_loop().sock_accept(cls.server_socket)
            asyncio.get_running_loop().create_task(cls.__discussion(connection))

    @classmethod
    async def __discussion(cls, connection):
        async with AsincSocketCloser(connection) as sock:
            while True:
                data = await asyncio.get_running_loop().sock_recv(sock, 1024)
                if not data:
                    break
                
                data = data.decode()
                json_data = json.loads(data) 
                json_list = (json_data['url'], json_data['headers'], json_data['json'])

                proxy_result = await cls.__get_data_from_server(*json_list)
                print('Yes')
                await asyncio.get_running_loop().sock_sendall(sock, proxy_result.send_data())

    @staticmethod
    async def __get_data_from_server(url, headers, json):
        async with aiohttp.ClientSession() as settion:
            async with settion.post(url, headers = headers, json = json) as result:
                if result.status != 200:
                    return ProxyResult('', result.status)
                
                return ProxyResult(await result.json(), result.status)
            
    @classmethod
    def main(cls):
        asyncio.run(cls.__listener())


if __name__ == '__main__':
    Server().main()