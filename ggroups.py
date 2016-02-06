import asyncio


@asyncio.coroutine
def handle_hello(reader, writer):
    peer = writer.get_extra_info('peername')
    writer.write("Hello, {0[0]}:{0[1]}!\n".format(peer).encode("utf-8"))
    writer.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    servers = []
    for i in range(3):
        print("Starting server {0}".format(i + 1))
        server = loop.run_until_complete(
            asyncio.start_server(handle_hello, '127.0.0.1', 8000 + i, loop=loop))
        servers.append(server)

    try:
        print("Running... Press ^C to shutdown")
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    for i, server in enumerate(servers):
        print("Closing server {0}".format(i + 1))
        server.close()
        loop.run_until_complete(server.wait_closed())
    loop.close()
