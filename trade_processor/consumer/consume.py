import asyncio
import os
import logging
import time

from aiokafka import AIOKafkaConsumer



async def consume():
    # from assets.services.price import PriceService
    # from orders.services.auto_order_finisher import AutoOrderFinisher
    consumer = AIOKafkaConsumer(
        'Assets',
        bootstrap_servers=os.environ.get('BOOTSTRAP_SERVERS'),
        group_id='my-consumer-group',
        auto_offset_reset='earliest',
    )
    await consumer.start()
    try:
        async for message in consumer:
            logging.info(f"Received message: {message.value.decode('utf-8')}")
            # asset = PriceService.update_price(message.value)
            # AutoOrderFinisher.check_opened_orders(asset)
    finally:
        await consumer.stop()


if __name__=='__main__':
    asyncio.run(consume())