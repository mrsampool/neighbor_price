import unittest
from unittest import mock
import pandas as pd
from typing import List
from io import StringIO

from components.event_manager.event_body import EventBody
from components.event_manager.event_manager_mock import EventManagerMock
from components.region_csv_endpoint_worker.region_csv_endpoint_worker import RegionCsvEndpointWorker
from data_collector.data_collector import DataCollector
from data_collector.tests.test_utils import MockResponse, dict_to_encoded_csv


def mocked_requests_get(*args, **kwargs) -> MockResponse:
    match args[0]:
        case 'csv/neighborhoods':
            content = dict_to_encoded_csv({
                "RegionId": ["region-id-1", "region-id-2"],
                "SizeRank": ["size-1", "size-2"],
                "RegionName": ["neighborhood-1", "neighborhood-2"],
                "RegionType": ["neighborhood", "neighborhood"],
                "StateName": ["state-name-1", "state-name-2"],
                "State": ["state-1", "state-2"],
                "City": ["city-1", "city-2"],
                "Metro": ["metro-1", "metro-2"],
                "CountyName": ["county-1", "county-2"],
                "2000-01-31": [100, 110],
                "2000-02-20": [200, 220]
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
            event_manager=EventManagerMock(publish_list=self.publish_list),
        )

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_collect_neighborhoods_data(self, mock):
        self.data_collector.collect_neighborhoods_data()
        actual_published = []
        for published in self.publish_list:
            actual_published.append(pd.read_csv(StringIO(published.data), index_col=0))

        actual_published_1 = actual_published[0]
        self.assertEqual("region-id-1", actual_published_1.loc['RegionId'][0])
        self.assertEqual("size-1", actual_published_1.loc["SizeRank"][0])
        self.assertEqual("neighborhood-1", actual_published_1.loc["RegionName"][0])
        self.assertEqual("neighborhood", actual_published_1.loc["RegionType"][0])
        self.assertEqual("state-name-1", actual_published_1.loc["StateName"][0])
        self.assertEqual("state-1", actual_published_1.loc["State"][0])
        self.assertEqual("city-1", actual_published_1.loc["City"][0])
        self.assertEqual("metro-1", actual_published_1.loc["Metro"][0])
        self.assertEqual("county-1", actual_published_1.loc["CountyName"][0])
        self.assertEqual("100", actual_published_1.loc["2000-01-31"][0])
        self.assertEqual("200", actual_published_1.loc["2000-02-20"][0])

        actual_published_2 = actual_published[1]
        self.assertEqual("region-id-2", actual_published_2.loc['RegionId'][0])
        self.assertEqual("size-2", actual_published_2.loc["SizeRank"][0])
        self.assertEqual("neighborhood-2", actual_published_2.loc["RegionName"][0])
        self.assertEqual("neighborhood", actual_published_2.loc["RegionType"][0])
        self.assertEqual("state-name-2", actual_published_2.loc["StateName"][0])
        self.assertEqual("state-2", actual_published_2.loc["State"][0])
        self.assertEqual("city-2", actual_published_2.loc["City"][0])
        self.assertEqual("metro-2", actual_published_2.loc["Metro"][0])
        self.assertEqual("county-2", actual_published_2.loc["CountyName"][0])
        self.assertEqual("110", actual_published_2.loc["2000-01-31"][0])
        self.assertEqual("220", actual_published_2.loc["2000-02-20"][0])

