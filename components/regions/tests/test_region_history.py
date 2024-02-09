import datetime
import unittest

from components.regions.region_record import RegionHistory, RegionHistoryItem, get_average_value_growth_rate


class TestRegionHistory(unittest.TestCase):

    def test_get_average_value_growth_rate(self):
        history = RegionHistory(
            items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 1),
                    region_value=100
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 1),
                    region_value=200
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 3, 1),
                    region_value=300
                )
            ]
        )
        actual_rate = get_average_value_growth_rate(region_history=history)
        expected_rate = 75.0
        self.assertEqual(expected_rate, actual_rate)

