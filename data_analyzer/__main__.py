#!/usr/bin/env python3
import json
import os
import pika
import sys
import logging

from components.event_manager.event_manager import EventManager
from components.zhvi.zhvi_data_gateway import ZhviDataGateway
from data_analyzer.data_analyzer import DataAnalyzer


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

        self.zhvi_db_uri = os.getenv("ZHVI_DB_URI")
        logging.info(f"using ZHVI_DB_URI: {self.zhvi_db_uri}")
        if self.zhvi_db_uri is None:
            logging.fatal("Missing required ENV: $ZHVI_DB_URI")

        self.zhvi_db_name = os.getenv("ZHVI_DB_NAME")
        logging.info(f"using ZHVI_DB_NAME: {self.zhvi_db_name}")
        if self.zhvi_db_name is None:
            logging.fatal("Missing required ENV: $ZHVI_DB_NAME")


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

    c = Config()

    zhvi_data_gateway = ZhviDataGateway(db_uri=c.zhvi_db_uri, db_name=c.zhvi_db_name)
    event_manager = EventManager(host=c.event_host, queue_name=c.event_lvhi_queue)
    data_analyzer = DataAnalyzer(event_manager=event_manager, zhvi_data_gateway=zhvi_data_gateway)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    data_analyzer.analyze()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
