import unittest
from unittest import mock
import pandas as pd
from typing import List
from io import StringIO

from components.event_manager.event_body import EventBody
from components.event_manager.event_manager_mock import EventManagerMock
from components.region_csv_endpoint_worker.region_csv_endpoint_worker import RegionCsvEndpointWorker
from data_collector.data_collector import DataCollector
from data_collector.tests.test_utils import mocked_requests_get


class TestDataCollector(unittest.TestCase):

    def setUp(self) -> None:

        csv_client = RegionCsvEndpointWorker(
            region_csv_url="csv/",
            neighborhood_csv_path="neighborhoods",
            metro_csv_path="metro",
            city_csv_path="city",
            state_csv_path="state"
        )

        self.publish_list: List[EventBody] = []

        self.data_collector = DataCollector(
            csv_client=csv_client,
            event_manager=EventManagerMock(publish_list=self.publish_list),
        )

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_collect_neighborhoods_data(self, mock):
        self.data_collector.collect_neighborhoods_data()
        actual_published = list(map(
            lambda published: pd.read_csv(StringIO(published.data), index_col=0),
            self.publish_list
        )),
        print(actual_published)

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
