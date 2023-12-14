import unittest
import logging
import os
import pandas as pd

from components.event_manager.event_manager import EventManager
from components.event_manager.event_body import EventBody
from components.zhvi.zhvi_data_gateway import ZhviDataGateway
from data_analyzer.data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self) -> None:
        event_host = os.getenv("EVENT_HOST")
        logging.info(f"using EVENT_HOST: {event_host}")
        if event_host is None:
            logging.fatal("Missing required ENV: $EVENT_HOST")

        event_zhvi_queue = os.getenv("EVENT_ZHVI_QUEUE")
        logging.info(f"using EVENT_ZHVI_QUEUE: {event_zhvi_queue}")
        if event_zhvi_queue is None:
            logging.fatal("Missing required ENV: $EVENT_ZHVI_QUEUE")

        zhvi_db_uri = os.getenv("ZHVI_DB_URI")
        logging.info(f"using ZHVI_DB_URI: {zhvi_db_uri}")
        if zhvi_db_uri is None:
            logging.fatal("Missing required ENV: $ZHVI_DB_URI")

        zhvi_db_name = os.getenv("ZHVI_DB_NAME")
        logging.info(f"using ZHVI_DB_NAME: {zhvi_db_name}")
        if zhvi_db_name is None:
            logging.fatal("Missing required ENV: $ZHVI_DB_NAME")

        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

        event_manager = EventManager(
            host=event_host,
            queue_name=event_zhvi_queue
        )

        data_gateway = ZhviDataGateway(db_uri=zhvi_db_uri, db_name=zhvi_db_name)

        self.data_analyzer = DataAnalyzer(event_manager=event_manager, zhvi_data_gateway=data_gateway)

    def test_analyze_data(self):
        df = pd.read_csv('./data/zhvi_neighborhoods.csv')
        df_row = df.loc[0]
        row_csv = df_row.to_csv()
        body = EventBody(
            name="collected zhvi record",
            data=row_csv
        ).to_json().encode('utf-8')
        self.data_analyzer.analyze_data(body=body)

