import asyncio

class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        print('data received: {}'.format(data.decode()))
        self.transport.write(data)

        # close the socket
        #self.transport.close()

    #def connection_lost(self):
    #    print('server closed the connection')



loop = asyncio.get_event_loop()
coro = loop.create_server(EchoServer, 'localhost', 8000)
server = loop.run_until_complete(coro)
print(server)
print(dir(server))
print(dir(server.sockets))

print('serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()