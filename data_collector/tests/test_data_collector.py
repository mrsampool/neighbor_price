import unittest
import logging
import os

from components.region_csv_endpoint_worker.region_csv_endpoint_worker import RegionCsvEndpointWorker
from components.event_manager.event_manager import EventManager
from data_collector.data_collector import DataCollector


class TestDataCollector(unittest.TestCase):

    def setUp(self) -> None:
        self.region_csv_url = os.getenv("REGION_CSV_URL")
        logging.info(f"using REGION_CSV_URL: {self.region_csv_url}")
        if self.region_csv_url is None:
            logging.fatal("Missing required ENV: $REGION_CSV_URL")

        self.neighborhood_csv_path = os.getenv("NEIGHBORHOOD_CSV_PATH")
        logging.info(f"using NEIGHBORHOOD_CSV_PATH: {self.neighborhood_csv_path}")
        if self.neighborhood_csv_path is None:
            logging.fatal("Missing required ENV: $NEIGHBORHOOD_CSV_PATH")

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

        self.event_region_queue = os.getenv("EVENT_REGION_QUEUE")
        logging.info(f"using EVENT_LVHI_QUEUE: {self.event_region_queue}")
        if self.event_region_queue is None:
            logging.fatal("Missing required ENV: $EVENT_REGION_QUEUE")

        csv_client = RegionCsvEndpointWorker(
            region_csv_url=self.region_csv_url,
            zvhi_neighborhood_csv_path=self.neighborhood_csv_path,
            zvhi_metro_csv_path=self.metro_csv_path,
            zvhi_state_csv_path=self.state_csv_path,
        )

        event_manager = EventManager(
            host=self.event_host,
            queue_name=self.event_region_queue
        )

        self.data_collector = DataCollector(
            csv_client=csv_client,
            event_manager=event_manager,
            region_data_gateway=None,
        )

    def test_collect_neighborhoods_data(self):
        self.data_collector.collect_neighborhoods_data()

"""

    def test_create_zhvi_neighborhood_from_df_row(self):
        neighborhood_df_row = pd.read_csv('../../data/zhvi_neighborhoods.csv')

        actual = create_zhvi_record_from_df_row(df_row=neighborhood_df_row.loc[0])
        self.assertEqual(actual.region_id, 112345)
        self.assertEqual(actual.size_rank, 0)
        self.assertEqual(actual.region_name, "Maryvale")
        self.assertEqual(actual.region_type, "neighborhood")
        self.assertEqual(actual.state_name, "AZ")
        self.assertEqual(actual.state, "AZ")
        self.assertEqual(actual.city, "Phoenix")
        self.assertEqual(actual.metro, "Phoenix-Mesa-Chandler, AZ")
        self.assertEqual(actual.county_name, "Maricopa County")

        actual_history = actual.zhvi_history
        actual_history_1 = actual_history[0]
        self.assertEqual(date.isoformat(actual_history_1.date), "2000-01-31")
        self.assertEqual(actual_history_1.zhvi_value, 75553.2814897809)
"""