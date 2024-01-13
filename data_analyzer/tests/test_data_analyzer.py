import unittest
import logging
import os
import pandas as pd

from components.event_manager.event_manager_pika import EventManagerPika
from components.event_manager.event_body import EventBody
from components.regions.region_data_gateway import RegionDataGateway
from data_analyzer.data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self) -> None:
        event_host = os.getenv("EVENT_HOST")
        logging.info(f"using EVENT_HOST: {event_host}")
        if event_host is None:
            logging.fatal("Missing required ENV: $EVENT_HOST")

        event_region_queue = os.getenv("EVENT_REGION_QUEUE")
        logging.info(f"using EVENT_REGION_QUEUE: {event_region_queue}")
        if event_region_queue is None:
            logging.fatal("Missing required ENV: $EVENT_REGION_QUEUE")

        region_db_uri = os.getenv("REGION_DB_URI")
        logging.info(f"using REGION_DB_URI: {region_db_uri}")
        if region_db_uri is None:
            logging.fatal("Missing required ENV: $REGION_DB_URI")

        region_db_name = os.getenv("REGION_DB_NAME")
        logging.info(f"using REGION_DB_NAME: {region_db_name}")
        if region_db_name is None:
            logging.fatal("Missing required ENV: $REGION_DB_NAME")

        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

        event_manager = EventManagerPika(
            host=event_host,
            queue_name=event_region_queue
        )

        data_gateway = RegionDataGateway(db_uri=region_db_uri, db_name=region_db_name)

        self.data_analyzer = DataAnalyzer(event_manager=event_manager, region_data_gateway=data_gateway)

    def test_analyze_data(self):
        df = pd.read_csv('./data/neighborhoods.csv')
        df_row = df.loc[0]
        row_csv = df_row.to_csv()
        body = EventBody(
            name="collected region record",
            data=row_csv
        ).to_json().encode('utf-8')
        self.data_analyzer.analyze_data(body=body)

