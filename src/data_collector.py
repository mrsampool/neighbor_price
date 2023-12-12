#!/usr/bin/env python3
from flask import Flask
import os
import logging

from components.zhvi_csv_client.zhvi_csv_client import ZhviCsvClient, create_zhvi_neighborhood_from_df_row
from components.zhvi_neighborhoods.zhvi_neighborhood_data_gateway import ZhviNeighborhoodDataGateway

app = Flask(__name__)


class Config:
    def __init__(self):
        self.zhvi_csv_url = os.getenv("ZHVI_CSV_URL")
        if self.zhvi_csv_url is None:
            logging.fatal("Missing required ENV: $ZHVI_CSV_URL")

        self.zhvi_neighborhood_csv_path = os.getenv("ZHVI_NEIGHBORHOOD_CSV_PATH")
        if self.zhvi_neighborhood_csv_path is None:
            logging.fatal("Missing required ENV: $ZHVI_NEIGHBORHOOD_CSV_PATH")

        self.zhvi_db_uri = os.getenv("ZHVI_DB_URI")
        if self.zhvi_db_uri is None:
            logging.fatal("Missing required ENV: $ZHVI_DB_URI")


def handler():
    c = Config()

    csv_client = ZhviCsvClient(
        zhvi_csv_url=c.zhvi_csv_url,
        zvhi_neighborhood_csv_path=c.zhvi_neighborhood_csv_path
    )

    zn_data_gateway = ZhviNeighborhoodDataGateway(app)

    neighborhoods_df = csv_client.get_zhvi_neighborhoods_df()
    for neighborhood in neighborhoods_df.iterrrows():
        neighborhood_record = create_zhvi_neighborhood_from_df_row(neighborhood)
        zn_data_gateway.create_neighborhood_record(record=neighborhood_record)


if __name__ == "__main__":
    handler()
