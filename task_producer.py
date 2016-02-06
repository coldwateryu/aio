import asyncio
import json

import aioamqp

message = {'fuck': 'this'}

async def new_task():
    try:
        transport, protocol = await aioamqp.connect()
    except aioamqp.AmqpClosedConnection:
        print("Connection's closed")
        return

    channel = await protocol.channel()

    await channel.queue_declare('task_queue', durable=True)

    await channel.basic_publish(
        payload=json.dumps(message),
        exchange_name='',
        routing_key='task_queue',
        properties={
            'delivery_mode': 2,
        },
    )
    print("Sent message {}".format(message))

    await protocol.close()
    transport.close()

asyncio.get_event_loop().run_until_complete(new_task())
