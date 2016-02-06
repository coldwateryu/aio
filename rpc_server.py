import asyncio
import aioamqp

import functools
import logging
import sys

MESSAGES = [
    b'This is the message. ',
    b'It will be sent ',
    b'in parts.',
]
SERVER_ADDRESS = ('127.0.0.1', 8888)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')


class FibHandler(asyncio.Protocol):

    def __init__(self, loop):
        super().__init__()
        self.log = logging.getLogger('FibHandler')

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug(
            'connecting to {} port {}'.format(*self.address)
        )

    async def handle(self, message):
        self.transport.write(message)
        self.log.debug('sending {!r}'.format(message))
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))

    def eof_received(self):
        self.log.debug('received EOF')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)

    def connection_lost(self, exc):
        self.log.debug('server closed connection')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)
        super().connection_lost(exc)


async def on_request(channel, body, envelope, properties):
    n = int(body)

    if n > 50:
        print(" [.] fuck off not doing anything bigger than 50.")
        response = 'fuck off not doing anything bigger than 50.'
    else:
        print(" [.] fib(%s)" % n)
        response = handler.handle(n)

    await channel.basic_publish(
        payload=str(response),
        exchange_name='',
        routing_key=properties.reply_to,
        properties={
            'correlation_id': properties.correlation_id,
        },
    )

    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)


async def rpc_server():
    transport, protocol = await aioamqp.connect()

    channel = await protocol.channel()

    await channel.queue_declare(queue_name='rpc_queue')
    await channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
    await channel.basic_consume(on_request, queue_name='rpc_queue')
    print(" [x] Awaiting RPC requests")


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(rpc_server())
event_loop.run_until_complete(tcp_echo_client(event_loop))
event_loop.run_forever()
