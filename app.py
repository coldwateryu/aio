import asyncio


# TCP client
class TcpClient(asyncio.Protocol):
    message = 'FUCK'

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write(self.message.encode())
        print('data sent: {}'.format(self.message))
        server_udp.tcp_client_connected()

    def data_received(self, data):
        self.data = format(data.decode())
        print('data received: {}'.format(data.decode()))
        if self.data == 'Testing':
            server_udp.send_data_to_udp(self.data)

    def send_data_to_tcp(self, data):
        print('sending some data using "send_data_to_tcp": {}'.format(data))
        self.transport.write(data.encode())

    def connection_lost(self, exc):
        msg = 'Connection lost with the server...'
        info = self.transport.get_extra_info('peername')
        server_udp.tcp_client_disconnected(msg, info)


# UDP Server
class UdpServer(asyncio.DatagramProtocol):
    CLIENT_TCP_TIMEOUT = 5.0

    def __init__(self):
        self.client_tcp_timeout = None

    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport

    def datagram_received(self, data, addr):
        self.data = data.strip()
        self.data = self.data.decode()
        print('Data should be sending to tcp:', self.data, addr)
        client_tcp[1].send_data_to_tcp(self.data)

    def connection_lost(self, exc):
        print('stop', exc)

    def send_data_to_udp(self, data):
        print('Receiving on UDPServer Class: ', (data))

    def connect_client_tcp(self):
        global client_tcp
        coro = loop.create_connection(TcpClient, 'localhost', 8000)
        task = asyncio.async(do_connect())

        def cb(result):
            client_tcp = result

        task.add_done_callback(cb)

    def tcp_client_disconnected(self, data, info):
        print(data)
        self.client_tcp_info = info
        self.client_tcp_timeout = loop.call_later(self.CLIENT_TCP_TIMEOUT, self.connect_client_tcp)

    def tcp_client_connected(self):
        if self.client_tcp_timeout:
            self.client_tcp_timeout.cancel()
            print('call_later cancel.')


@asyncio.coroutine
def do_connect():
    global client_tcp
    while True:
        try:
            client_tcp = yield from loop.create_connection(TcpClient, 'localhost', 8000)
        except OSError:
            print("Server not up retrying in 5 seconds...")
            yield from asyncio.sleep(5)
        else:
            break


loop = asyncio.get_event_loop()

# UDP Server
coro = loop.create_datagram_endpoint(UdpServer, local_addr=('localhost', 9000))
transport, server_udp = loop.run_until_complete(coro)

# TCP client
loop.run_until_complete(do_connect())

loop.run_forever()
