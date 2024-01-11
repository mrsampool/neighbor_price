import unittest
from unittest import mock
import pandas as pd
from dataclasses import dataclass
from typing import List
from io import StringIO

from components.event_manager.event_body import EventBody
from components.region_csv_endpoint_worker.region_csv_endpoint_worker import RegionCsvEndpointWorker
from components.event_manager.event_manager import EventManager
from data_collector.data_collector import DataCollector


@dataclass
class MockResponse:
    content: bytes


@dataclass
class MockEventManager(EventManager):

    def __init__(self, publish_list: List[EventBody]):
        super().__init__(channel="x")
        self.published: List[EventBody] = publish_list

    def publish(self, body: EventBody):
        self.published.append(body)


def mocked_requests_get(*args, **kwargs) -> MockResponse:

    def dict_to_encoded_csv(dict_data: dict) -> bytes:
        df = pd.DataFrame(dict_data)
        csv_string = df.to_csv(index=False)
        return csv_string.encode('utf-8')

    match args[0]:
        case 'csv/neighborhoods':
            # RegionID,SizeRank,RegionName,RegionType,StateName,State,City,Metro,CountyName,2000-01-31,2000-02-29,

            content = dict_to_encoded_csv({
                "RegionId": ["region-id-1"],
                "SizeRank": ["size-1"],
                "RegionName": ["region-1"],
                "RegionType": ["neighborhood"],
                "StateName": ["state-1"],
                "State": ["state-1"],
                "City": ["city-1"],
                "Metro": ["metro-1"],
                "CountyName": ["county-1"],
                "2000-01-31": [100],
                "2000-02-20": [200]
            })
            return MockResponse(content=content)


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
            event_manager=MockEventManager(publish_list=self.publish_list),
        )

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
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
