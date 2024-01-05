import unittest
from typing import List
from datetime import datetime

from components.regions.region_record import RegionRecord, RegionHistoryItem
from components.regions.region_data_gateway import RegionDataGateway
from neighbor_price.region_detail import RegionDetail


class MockRegionDataGateway(RegionDataGateway):

    def __init__(self):
        super().__init__(collection="x")

    def get_us_doc(self) -> RegionRecord:
        return RegionRecord(
            region_id="0",
            region_history=[
                RegionHistoryItem(
                    date=datetime(2023, 1, 1),
                    region_vale=130
                ),
                RegionHistoryItem(
                    date=datetime(2023, 2, 1),
                    region_vale=140
                )
            ]
        )

    def get_region_by_id(self, region_id):
        match region_id:
            case "1":
                return RegionRecord(
                    region_name="Colorado",
                    region_history=[
                        RegionHistoryItem(
                            date=datetime(2023, 1, 1),
                            region_vale=150
                        ),
                        RegionHistoryItem(
                            date=datetime(2023, 2, 1),
                            region_vale=160
                        )
                    ]
                )

    def get_all_metros_for_state(self, state_name) -> List[RegionRecord]:
        if state_name == "Colorado":
            return [
                RegionRecord(
                    region_id="2",
                    region_name="metro-1"
                ),
                RegionRecord(
                    region_id="3",
                    region_name="metro-2"
                )
            ]


class TestRegionDetailState(unittest.TestCase):

    def setUp(self) -> None:
        self.region_detail = RegionDetail(
            region_data_gateway=MockRegionDataGateway(),
            state_id="1",
        )

    def test_region_detail_state_record(self):
        self.assertEqual(
            self.region_detail.region_records.state.region_name,
            "Colorado"
        )

    def test_region_detail_state_links(self):
        self.assertEqual(
            self.region_detail.region_links.links[0].address,
            "/state/1/metro/2",
        )
        self.assertEqual(
            self.region_detail.region_links.links[0].label,
            "metro-1",
        )
        self.assertEqual(
            self.region_detail.region_links.links[1].address,
            f"/state/1/metro/3",
        )
        self.assertEqual(
            self.region_detail.region_links.links[1].label,
            "metro-2",
        )

    def test_region_detail_state_prices(self):
        self.assertEqual(self.region_detail.prices.state[0], 150)
        self.assertEqual(self.region_detail.prices.state[1], 160)

    def test_region_detail_state_dates(self):
        self.assertEqual(self.region_detail.dates[0].strftime("%m/%d/%Y"), "01/01/2023")
        self.assertEqual(self.region_detail.dates[1].strftime("%m/%d/%Y"), "02/01/2023")


"""
    def test_region_detail_metro(self):
        self.region_detail = RegionDetail(
            region_data_gateway=self.region_data_gateway,
            state_id="10",
            metro_id="394530",
        )

    def test_region_detail_city(self):
        self.region_detail = RegionDetail(
            region_data_gateway=self.region_data_gateway,
            state_id="10",
            metro_id="394530",
        )

    def test_region_detail_neighborhood(self):
        self.region_detail = RegionDetail(
            region_data_gateway=self.region_data_gateway,
            state_id="10",
            metro_id="394530",
            neighborhood_id="268743"
        )

"""
