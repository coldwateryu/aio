import asyncio
import socket
import aioamqp


@asyncio.coroutine
def error_callback(exception):
    print(exception)


@asyncio.coroutine
def connect():
    try:
        transport, protocol = yield from aioamqp.connect(
            host='nonexistant.com',
            on_error=error_callback,
            client_properties={
                'program_name': "test",
                'hostname': socket.gethostname(),
            },

        )
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return
    except ConnectionRefusedError:
        print("fucking hell")
        return


asyncio.get_event_loop().run_until_complete(connect())
