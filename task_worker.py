import asyncio
import json

import aioamqp

async def callback(channel, body, envelope, properties):
    if isinstance(body, bytes):
        body = body.decode('utf-8')

    if isinstance(body, str):
        body = json.loads(body)

    print("Received a fuck message. It says fuck what? Fuck: {}".format(body['fuck']))
    await asyncio.sleep(3)
    print("Processing done")
    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)

async def worker():
    try:
        transport, protocol = await aioamqp.connect()
    except aioamqp.AmqpClosedConnection:
        print("Connection's closed")
        return

    channel = await protocol.channel()

    await channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
    await channel.basic_consume(callback=callback, queue_name='task_queue')


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(worker())
event_loop.run_forever()
