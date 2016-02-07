import asyncio


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


async def handle(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        if isinstance(message, str):
            response = message
        elif all((isinstance(message, dict), 'command' in message, message['command'] == "fib")):
            response = fib(int(message['payload']))
        else:
            response = 'only fib here bitch'

        print("Send: %r" % message)
        writer.write(response.encode(encoding='utf-8'))
        await writer.drain()

    # print("Close the client socket")
    # writer.close()

loop = asyncio.get_event_loop()
loop.set_debug(enabled=True)
coro = asyncio.start_server(handle, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
