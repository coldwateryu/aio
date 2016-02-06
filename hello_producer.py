import asyncio
import aioamqp


async def connect():
    transport, protocol = await aioamqp.connect()
    channel = await protocol.channel()

    await channel.exchange_declare(type_name='fanout', exchange_name='the_exchange')

    await channel.queue_declare(queue_name='hello')
    await channel.queue_bind(queue_name='hello', exchange_name='the_exchange', routing_key='whatever')

    await channel.queue_declare(queue_name='hi')
    await channel.queue_bind(queue_name='hi', exchange_name='the_exchange', routing_key='whatever')

    await channel.queue_purge(queue_name='hi')
    await channel.queue_purge(queue_name='hello')

    for x in range(10):
        await channel.basic_publish(
            payload='Fuck this shit. HELLo World! {}'.format(x),
            exchange_name='the_exchange',
            routing_key='whatever'
        )
        print('sent hello message no {}'.format(x))
    await protocol.close()
    transport.close()

asyncio.get_event_loop().run_until_complete(connect())
