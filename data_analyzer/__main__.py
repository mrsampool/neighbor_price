#!/usr/bin/env python3
import json
import os
import pika
import sys
import logging

from components.event_manager.event_manager import EventManager


class Config:
    def __init__(self):
        self.event_host = os.getenv("EVENT_HOST")
        logging.info(f"using EVENT_HOST: {self.event_host}")
        if self.event_host is None:
            logging.fatal("Missing required ENV: $EVENT_HOST")

        self.event_lvhi_queue = os.getenv("EVENT_ZHVI_QUEUE")
        logging.info(f"using EVENT_ZHVI_QUEUE: {self.event_lvhi_queue}")
        if self.event_lvhi_queue is None:
            logging.fatal("Missing required ENV: $EVENT_ZHVI_QUEUE")


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

    c = Config()

    event_manager = EventManager(
        host=c.event_host,
        queue_name=c.event_lvhi_queue
    )

    def callback(ch, method, properties, body):
        body = json.loads(body)
        print(" [x] Received %r" % body)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    event_manager.consume(callback=callback)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
