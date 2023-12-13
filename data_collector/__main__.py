#!/usr/bin/env python3
from flask import Flask
import os
import logging
from data_collector.data_collector import DataCollector

from components.zhvi_csv_client.zhvi_csv_client import ZhviCsvClient
from components.zhvi.zhvi_data_gateway import ZhviDataGateway

app = Flask(__name__)


class Config:
    def __init__(self):
        self.zhvi_db_uri = os.getenv("ZHVI_DB_URI")
        logging.info(f"using ZHVI_DB_URI: {self.zhvi_db_uri}")
        if self.zhvi_db_uri is None:
            logging.fatal("Missing required ENV: $ZHVI_DB_URI")

        self.zhvi_db_name = os.getenv("ZHVI_DB_NAME")
        logging.info(f"using ZHVI_DB_NAME: {self.zhvi_db_name}")
        if self.zhvi_db_name is None:
            logging.fatal("Missing required ENV: $ZHVI_DB_NAME")

        self.zhvi_csv_url = os.getenv("ZHVI_CSV_URL")
        logging.info(f"using ZHVI_CSV_URL: {self.zhvi_csv_url}")
        if self.zhvi_csv_url is None:
            logging.fatal("Missing required ENV: $ZHVI_CSV_URL")

        self.zhvi_neighborhood_csv_path = os.getenv("ZHVI_NEIGHBORHOOD_CSV_PATH")
        logging.info(f"using ZHVI_NEIGHBORHOOD_CSV_PATH: {self.zhvi_neighborhood_csv_path}")
        if self.zhvi_neighborhood_csv_path is None:
            logging.fatal("Missing required ENV: $ZHVI_NEIGHBORHOOD_CSV_PATH")

        self.zhvi_metro_csv_path = os.getenv("ZHVI_METRO_CSV_PATH")
        logging.info(f"using ZHVI_METRO_CSV_PATH: {self.zhvi_metro_csv_path}")
        if self.zhvi_metro_csv_path is None:
            logging.fatal("Missing required ENV: $ZHVI_METRO_CSV_PATH")

        self.zhvi_state_csv_path = os.getenv("ZHVI_STATE_CSV_PATH")
        logging.info(f"using ZHVI_STATE_CSV_PATH: {self.zhvi_state_csv_path}")
        if self.zhvi_state_csv_path is None:
            logging.fatal("Missing required ENV: $ZHVI_STATE_CSV_PATH")


def handler():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

    c = Config()

    csv_client = ZhviCsvClient(
        zhvi_csv_url=c.zhvi_csv_url,
        zvhi_neighborhood_csv_path=c.zhvi_neighborhood_csv_path,
        zvhi_metro_csv_path=c.zhvi_metro_csv_path,
        zvhi_state_csv_path=c.zhvi_state_csv_path,
    )

    zhvi_data_gateway = ZhviDataGateway(
        db_uri=c.zhvi_db_uri,
        db_name=c.zhvi_db_name
    )

    data_collector = DataCollector(
        csv_client=csv_client,
        zhvi_data_gateway=zhvi_data_gateway,
    )

    data_collector.collect_neighborhoods_data()
    data_collector.collect_metros_data()
    data_collector.collect_states_data()


if __name__ == "__main__":
    handler()
