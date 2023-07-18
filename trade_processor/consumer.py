import json
import os

import django
from kafka import KafkaConsumer

django.setup()

from assets.services.price import PriceService
from orders.services.auto_order_finisher import AutoOrderFinisher


def consume():

    consumer = KafkaConsumer(
        'Assets',
        bootstrap_servers=os.environ.get('BOOTSTRAP_SERVERS'),
        group_id='my-consumer-group',
        auto_offset_reset='earliest',
    )

    for message in consumer:
        asset = PriceService.update_price(
            json.loads(message.value.decode('utf-8'))
        )
        AutoOrderFinisher.check_opened_orders(asset)


if __name__ == '__main__':
    consume()
