#!/usr/bin/env python3
import os
import logging
from data_collector.data_collector import DataCollector

from components.region_csv_endpoint_worker.region_csv_endpoint_worker import RegionCsvEndpointWorker
from components.regions.region_data_gateway_mongo import RegionDataGatewayMongo
from components.event_manager.event_manager_pika import EventManagerPika


class Config:
    def __init__(self):
        self.region_db_uri = os.getenv("REGION_DB_URI")
        logging.info(f"using REGION_DB_URI: {self.region_db_uri}")
        if self.region_db_uri is None:
            logging.fatal("Missing required ENV: $REGION_DB_URI")

        self.region_db_name = os.getenv("REGION_DB_NAME")
        logging.info(f"using REGION_DB_NAME: {self.region_db_name}")
        if self.region_db_name is None:
            logging.fatal("Missing required ENV: $REGION_DB_NAME")

        self.region_csv_url = os.getenv("REGION_CSV_URL")
        logging.info(f"using REGION_CSV_URL: {self.region_csv_url}")
        if self.region_csv_url is None:
            logging.fatal("Missing required ENV: $REGION_CSV_URL")

        self.neighborhood_csv_path = os.getenv("NEIGHBORHOOD_CSV_PATH")
        logging.info(f"using NEIGHBORHOOD_CSV_PATH: {self.neighborhood_csv_path}")
        if self.neighborhood_csv_path is None:
            logging.fatal("Missing required ENV: $NEIGHBORHOOD_CSV_PATH")

        self.city_csv_path = os.getenv("CITY_CSV_PATH")
        logging.info(f"using CITY_CSV_PATH: {self.city_csv_path}")
        if self.city_csv_path is None:
            logging.fatal("Missing required ENV: $CITY_CSV_PATH")

        self.metro_csv_path = os.getenv("METRO_CSV_PATH")
        logging.info(f"using METRO_CSV_PATH: {self.metro_csv_path}")
        if self.metro_csv_path is None:
            logging.fatal("Missing required ENV: $METRO_CSV_PATH")

        self.state_csv_path = os.getenv("STATE_CSV_PATH")
        logging.info(f"using STATE_CSV_PATH: {self.state_csv_path}")
        if self.state_csv_path is None:
            logging.fatal("Missing required ENV: $STATE_CSV_PATH")

        self.event_host = os.getenv("EVENT_HOST")
        logging.info(f"using EVENT_HOST: {self.event_host}")
        if self.event_host is None:
            logging.fatal("Missing required ENV: $EVENT_HOST")

        self.event_lvhi_queue = os.getenv("EVENT_REGION_QUEUE")
        logging.info(f"using EVENT_REGION_QUEUE: {self.event_lvhi_queue}")
        if self.event_lvhi_queue is None:
            logging.fatal("Missing required ENV: $EVENT_REGION_QUEUE")


def handler():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

    c = Config()

    csv_client = RegionCsvEndpointWorker(
        region_csv_url=c.region_csv_url,
        neighborhood_csv_path=c.neighborhood_csv_path,
        city_csv_path=c.city_csv_path,
        metro_csv_path=c.metro_csv_path,
        state_csv_path=c.state_csv_path,
    )

    region_data_gateway = RegionDataGatewayMongo(
        db_uri=c.region_db_uri,
        db_name=c.region_db_name
    )

    event_manager = EventManagerPika(
        host=c.event_host,
        queue_name=c.event_lvhi_queue
    )

    data_collector = DataCollector(
        csv_client=csv_client,
        event_manager=event_manager
    )

    data_collector.collect_neighborhoods_data()
    data_collector.collect_cities_data()
    data_collector.collect_metros_data()
    data_collector.collect_states_data()


if __name__ == "__main__":
    handler()
