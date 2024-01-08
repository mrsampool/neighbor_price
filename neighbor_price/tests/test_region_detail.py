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
            case "2":
                return RegionRecord(
                    region_name="metro-1",
                    state_name="CO",
                    region_history=[
                        RegionHistoryItem(
                            date=datetime(2023, 1, 1),
                            region_vale=170
                        ),
                        RegionHistoryItem(
                            date=datetime(2023, 2, 1),
                            region_vale=180
                        )
                    ]
                )
            case "4":
                return RegionRecord(
                    region_name="city-1",
                    state_name="CO",
                    region_history=[
                        RegionHistoryItem(
                            date=datetime(2023, 1, 1),
                            region_vale=190
                        ),
                        RegionHistoryItem(
                            date=datetime(2023, 2, 1),
                            region_vale=200
                        )
                    ]
                )
            case "7":
                return RegionRecord(
                    region_name="neighborhood-1",
                    state_name="CO",
                    region_history=[
                        RegionHistoryItem(
                            date=datetime(2023, 1, 1),
                            region_vale=210
                        ),
                        RegionHistoryItem(
                            date=datetime(2023, 2, 1),
                            region_vale=220
                        )
                    ]
                )

    def get_all_metros_for_state(self, state_name) -> List[RegionRecord]:
        match state_name:
            case "Colorado":
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

    def get_all_cities_for_metro(self, metro_name, state_abbrev) -> List[RegionRecord]:
        if metro_name == "metro-1" and state_abbrev == "CO":
            return [
                RegionRecord(
                    region_id="4",
                    region_name="city-1"
                ),
                RegionRecord(
                    region_id="5",
                    region_name="city-2"
                ),
            ]

    def get_all_neighborhoods_for_city(self, city_name, state_abbrev) -> List[RegionRecord]:
        if city_name == "city-1" and state_abbrev == "CO":
            return [
                RegionRecord(
                    region_id="6",
                    region_name="neighborhood-1"
                ),
                RegionRecord(
                    region_id="7",
                    region_name="neighborhood-2"
                ),
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


class TestRegionDetailMetro(unittest.TestCase):

    def setUp(self) -> None:
        self.region_detail = RegionDetail(
            region_data_gateway=MockRegionDataGateway(),
            state_id="1",
            metro_id="2"
        )

    def test_region_detail_metro_records(self):
        self.assertEqual(
            self.region_detail.region_records.state.region_name,
            "Colorado"
        )
        self.assertEqual(
            self.region_detail.region_records.metro.region_name,
            "metro-1"
        )

    def test_region_detail_metro_links(self):
        self.assertEqual(
            self.region_detail.region_links.links[0].address,
            "/state/1/metro/2/city/4",
        )
        self.assertEqual(
            self.region_detail.region_links.links[0].label,
            "city-1",
        )
        self.assertEqual(
            self.region_detail.region_links.links[1].address,
            f"/state/1/metro/2/city/5",
        )
        self.assertEqual(
            self.region_detail.region_links.links[1].label,
            "city-2",
        )

    def test_region_detail_metro_prices(self):
        self.assertEqual(self.region_detail.prices.state[0], 150)
        self.assertEqual(self.region_detail.prices.state[1], 160)

        self.assertEqual(self.region_detail.prices.metro[0], 170)
        self.assertEqual(self.region_detail.prices.metro[1], 180)

    def test_region_detail_metro_dates(self):
        self.assertEqual(self.region_detail.dates[0].strftime("%m/%d/%Y"), "01/01/2023")
        self.assertEqual(self.region_detail.dates[1].strftime("%m/%d/%Y"), "02/01/2023")


class TestRegionDetailCity(unittest.TestCase):

    def setUp(self) -> None:
        self.region_detail = RegionDetail(
            region_data_gateway=MockRegionDataGateway(),
            state_id="1",
            metro_id="2",
            city_id="4"
        )

    def test_region_detail_city_records(self):
        self.assertEqual(
            self.region_detail.region_records.state.region_name,
            "Colorado"
        )
        self.assertEqual(
            self.region_detail.region_records.metro.region_name,
            "metro-1"
        )
        self.assertEqual(
            self.region_detail.region_records.city.region_name,
            "city-1"
        )

    def test_region_detail_city_links(self):
        self.assertEqual(
            self.region_detail.region_links.links[0].address,
            "/state/1/metro/2/city/4/neighborhood/6",
        )
        self.assertEqual(
            self.region_detail.region_links.links[0].label,
            "neighborhood-1",
        )
        self.assertEqual(
            self.region_detail.region_links.links[1].address,
            f"/state/1/metro/2/city/4/neighborhood/7",
        )
        self.assertEqual(
            self.region_detail.region_links.links[1].label,
            "neighborhood-2",
        )

    def test_region_detail_city_prices(self):
        self.assertEqual(self.region_detail.prices.state[0], 150)
        self.assertEqual(self.region_detail.prices.state[1], 160)

        self.assertEqual(self.region_detail.prices.metro[0], 170)
        self.assertEqual(self.region_detail.prices.metro[1], 180)

        self.assertEqual(self.region_detail.prices.city[0], 190)
        self.assertEqual(self.region_detail.prices.city[1], 200)

    def test_region_detail_city_dates(self):
        self.assertEqual(self.region_detail.dates[0].strftime("%m/%d/%Y"), "01/01/2023")
        self.assertEqual(self.region_detail.dates[1].strftime("%m/%d/%Y"), "02/01/2023")


class TestRegionDetailNeighborhood(unittest.TestCase):

    def setUp(self) -> None:
        self.region_detail = RegionDetail(
            region_data_gateway=MockRegionDataGateway(),
            state_id="1",
            metro_id="2",
            city_id="4",
            neighborhood_id="7"
        )

    def test_region_detail_neighborhood_records(self):
        self.assertEqual(
            self.region_detail.region_records.state.region_name,
            "Colorado"
        )
        self.assertEqual(
            self.region_detail.region_records.metro.region_name,
            "metro-1"
        )
        self.assertEqual(
            self.region_detail.region_records.city.region_name,
            "city-1"
        )
        self.assertEqual(
            self.region_detail.region_records.neighborhood.region_name,
            "neighborhood-1"
        )

    def test_region_detail_neighborhood_links(self):
        self.assertEqual(
            self.region_detail.region_links.links,
            [],
        )

    def test_region_detail_neighborhood_prices(self):
        self.assertEqual(self.region_detail.prices.state[0], 150)
        self.assertEqual(self.region_detail.prices.state[1], 160)

        self.assertEqual(self.region_detail.prices.metro[0], 170)
        self.assertEqual(self.region_detail.prices.metro[1], 180)

        self.assertEqual(self.region_detail.prices.city[0], 190)
        self.assertEqual(self.region_detail.prices.city[1], 200)

        self.assertEqual(self.region_detail.prices.neighborhood[0], 210)
        self.assertEqual(self.region_detail.prices.neighborhood[1], 220)

    def test_region_detail_neighborhood_dates(self):
        self.assertEqual(self.region_detail.dates[0].strftime("%m/%d/%Y"), "01/01/2023")
        self.assertEqual(self.region_detail.dates[1].strftime("%m/%d/%Y"), "02/01/2023")