import unittest
from typing import List

import pandas as pd

from components.event_manager.event_manager_mock import EventManagerMock
from components.event_manager.event_body import EventBody
from components.regions.region_data_gateway_mock import RegionDataGatewayMock
from components.regions.region_record import RegionRecord
from data_analyzer.data_analyzer import DataAnalyzer


class TestDataAnalyzer(unittest.TestCase):
    def setUp(self) -> None:
        self.save_list: List[RegionRecord] = []
        self.data_analyzer = DataAnalyzer(
            event_manager=EventManagerMock(),
            region_data_gateway=RegionDataGatewayMock(save_list=self.save_list)
        )

    def test_analyze_data(self):
        df = pd.DataFrame(data={
            "RegionId": ["region-id-1"],
            "SizeRank": ["size-1"],
            "RegionName": ["neighborhood-1"],
            "RegionType": ["neighborhood"],
            "StateName": ["state-name-1"],
            "State": ["state-1"],
            "City": ["city-1"],
            "Metro": ["metro-1"],
            "CountyName": ["county-1"],
            "2000-01-31": [100],
            "2000-02-20": [200]
        })
        row_csv = ',0\nRegionId,region-id-1\nSizeRank,size-1\nRegionName,state-1\nRegionType,state\nStateName,State,\nCity,\nMetro,\nCountyName,\n2000-01-31,70\n2000-02-20,170'

        body = EventBody(
            name="collected region record",
            data=row_csv
        ).to_json().encode('utf-8')

        self.data_analyzer.analyze_data(body=body)

        actual_saved = self.save_list[0]

        self.assertEqual("region-id-1", actual_saved.region_id)
        self.assertEqual("size-1", actual_saved.size_rank)
        self.assertEqual("neighborhood-1", actual_saved.region_name)
        self.assertEqual("neighborhood", actual_saved.region_type)
        self.assertEqual("state-name-1", actual_saved.state_name)
        self.assertEqual("state-1", actual_saved.state)
        self.assertEqual("city-1", actual_saved.city)
        self.assertEqual("metro-1", actual_saved.metro)
        self.assertEqual("county-1", actual_saved.county_name)

        actual_history = actual_saved.region_history
        actual_history_1 = actual_history.history_items[0]
        self.assertEqual("2000-01-31", actual_history_1.date)
        self.assertEqual(100, actual_history_1.region_value)

        actual_history_2 = actual_history.history_items[1]
        self.assertEqual("2000-02-20", actual_history_2.date)
        self.assertEqual(200, actual_history_2.region_value)

