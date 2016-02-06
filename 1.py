import asyncio
import aioamqp

@asyncio.coroutine
def connect():
    try:
        transport, protocol = yield from aioamqp.connect()  # use default parameters
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    print("connected !")
    yield from asyncio.sleep(1)

    print("close connection")
    yield from protocol.close()
    transport.close()

asyncio.get_event_loop().run_until_complete(connect())
