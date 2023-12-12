#!/usr/bin/env python3
from flask import Flask
import os
import logging

from components.zhvi_csv_client.zhvi_csv_client import ZhviCsvClient, create_zhvi_neighborhood_from_df_row
from components.zhvi_neighborhoods.zhvi_neighborhood_data_gateway import ZhviNeighborhoodDataGateway

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
    c = Config()

    csv_client = ZhviCsvClient(
        zhvi_csv_url=c.zhvi_csv_url,
        zvhi_neighborhood_csv_path=c.zhvi_neighborhood_csv_path,
        zvhi_metro_csv_path=c.zhvi_metro_csv_path,
        zvhi_state_csv_path=c.zhvi_state_csv_path,
    )

    zn_data_gateway = ZhviNeighborhoodDataGateway(db_uri=c.zhvi_db_uri, db_name=c.zhvi_db_name)

    neighborhoods_df = csv_client.get_zhvi_neighborhoods_df()
    for _, neighborhood in neighborhoods_df.iterrows():
        neighborhood_record = create_zhvi_neighborhood_from_df_row(neighborhood)
        zn_data_gateway.create_neighborhood_record(record=neighborhood_record)


if __name__ == "__main__":
    handler()
