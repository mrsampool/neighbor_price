#!/usr/bin/env python3
import json
import os
import pika
import sys
import logging

from components.event_manager.event_manager_pika import EventManagerPika
from components.regions.region_data_gateway import RegionDataGateway
from data_analyzer.data_analyzer import DataAnalyzer


class Config:
    def __init__(self):
        self.event_host = os.getenv("EVENT_HOST")
        logging.info(f"using EVENT_HOST: {self.event_host}")
        if self.event_host is None:
            logging.fatal("Missing required ENV: $EVENT_HOST")

        self.event_lvhi_queue = os.getenv("EVENT_REGION_QUEUE")
        logging.info(f"using EVENT_REGION_QUEUE: {self.event_lvhi_queue}")
        if self.event_lvhi_queue is None:
            logging.fatal("Missing required ENV: $EVENT_REGION_QUEUE")

        self.regions_db_uri = os.getenv("REGION_DB_URI")
        logging.info(f"using REGION_DB_URI: {self.regions_db_uri}")
        if self.regions_db_uri is None:
            logging.fatal("Missing required ENV: $REGION_DB_URI")

        self.regions_db_name = os.getenv("REGION_DB_NAME")
        logging.info(f"using REGION_DB_NAME: {self.regions_db_name}")
        if self.regions_db_name is None:
            logging.fatal("Missing required ENV: $REGION_DB_NAME")


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

    c = Config()

    region_data_gateway = RegionDataGateway(db_uri=c.regions_db_uri, db_name=c.regions_db_name)
    event_manager = EventManagerPika(host=c.event_host, queue_name=c.event_lvhi_queue)
    data_analyzer = DataAnalyzer(event_manager=event_manager, region_data_gateway=region_data_gateway)

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
