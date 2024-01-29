#!/usr/bin/env python3
import os
import sys
import logging

from components.event_manager.event_manager_pika import EventManagerPika
from components.event_manager.event_manager import EVENT_QUEUE_MODE_RABBITMQ, EVENT_QUEUE_MODE_SNS
from components.regions.region_data_gateway_mongo import RegionDataGatewayMongo
from data_analyzer.data_analyzer import DataAnalyzer


class Config:
    def __init__(self, event_queue_mode: str):

        self.regions_db_uri = os.getenv("REGION_DB_URI")
        logging.info(f"using REGION_DB_URI: {self.regions_db_uri}")
        if self.regions_db_uri is None:
            logging.fatal("Missing required ENV: $REGION_DB_URI")

        self.regions_db_name = os.getenv("REGION_DB_NAME")
        logging.info(f"using REGION_DB_NAME: {self.regions_db_name}")
        if self.regions_db_name is None:
            logging.fatal("Missing required ENV: $REGION_DB_NAME")

        if event_queue_mode == EVENT_QUEUE_MODE_RABBITMQ:

            self.event_rabbit_mq_host = os.getenv("EVENT_RABBITMQ_HOST")
            if self.event_rabbit_mq_host is None:
                logging.fatal("Missing required ENV: $EVENT_RABBITMQ_HOST")
            logging.info(f"using EVENT_RABBITMQ_HOST: {self.event_rabbit_mq_host}")

            self.event_rabbitmq_queue = os.getenv("EVENT_RABBITMQ_QUEUE")
            if self.event_rabbitmq_queue is None:
                logging.fatal("Missing required ENV: $EVENT_RABBITMQ_QUEUE")
            logging.info(f"using EVENT_RABBITMQ_QUEUE: {self.event_rabbitmq_queue}")

        elif event_queue_mode == EVENT_QUEUE_MODE_SNS:

            self.event_sns_region = os.getenv("EVENT_SNS_REGION")
            logging.info(f"using EVENT_SNS_REGION: {self.event_sns_region}")
            if self.event_sns_region is None:
                logging.fatal("Missing required ENV: $EVENT_SNS_REGION")

            self.event_sns_topic_arn = os.getenv("EVENT_SNS_TOPIC_ARN")
            logging.info(f"using EVENT_SNS_TOPIC_ARN: {self.event_sns_topic_arn}")
            if self.event_sns_topic_arn is None:
                logging.fatal("Missing required ENV: $EVENT_SNS_TOPIC_ARN")

        else:
            logging.fatal(f"UNSUPPORTED EVENT_QUEUE_MODE: {event_queue_mode}")


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

    c = Config(event_queue_mode=EVENT_QUEUE_MODE_RABBITMQ)

    region_data_gateway = RegionDataGatewayMongo(db_uri=c.regions_db_uri, db_name=c.regions_db_name)
    event_manager = EventManagerPika(host=c.event_rabbit_mq_host, queue_name=c.event_rabbitmq_queue)
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
