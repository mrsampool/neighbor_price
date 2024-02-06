import unittest

from components.regions.region_data_gateway_mock import RegionDataGatewayMock
from components.regions.region_record import RegionRecord
from neighbor_price.region_detailer import RegionDetailer
from neighbor_price.region_details import RegionRecords


class TestRegionDetailUS(unittest.TestCase):

    def setUp(self) -> None:
        region_detailer = RegionDetailer(data_gateway=RegionDataGatewayMock())
        self.region_detail = region_detailer.get_us_detail()

    def test_region_detail_us_records(self):
        self.assertEqual(
            self.region_detail.region_records.us.region_name,
            "United States of America"
        )

    def test_region_detail_us_links(self):
        self.assertEqual(
            self.region_detail.links[0].address,
            "/state/state-1-id",
        )
        self.assertEqual(
            self.region_detail.links[0].label,
            "state-1-name",
        )
        self.assertEqual(
            self.region_detail.links[1].address,
            f"/state/state-2-id",
        )
        self.assertEqual(
            self.region_detail.links[1].label,
            "state-2-name",
        )

    def test_region_detail_us_prices(self):
        self.assertEqual(self.region_detail.prices.us[0], 130)
        self.assertEqual(self.region_detail.prices.us[1], 140)

    def test_region_detail_us_dates(self):
        self.assertEqual(self.region_detail.dates[0], "2023-01")
        self.assertEqual(self.region_detail.dates[1], "2023-02")


class TestRegionDetailState(unittest.TestCase):

    def setUp(self) -> None:
        region_detailer = RegionDetailer(data_gateway=RegionDataGatewayMock())
        self.region_detail = region_detailer.get_state_detail(state_id="1")

    def test_region_detail_state_records(self):
        self.assertEqual(
            self.region_detail.region_records.state.region_name,
            "Colorado"
        )

    def test_region_detail_state_links(self):
        self.assertEqual(
            "/state/1/metro/2",
            self.region_detail.links[0].address,
        )
        self.assertEqual(
            "metro-1",
            self.region_detail.links[0].label,
        )
        self.assertEqual(
            f"/state/1/metro/3",
            self.region_detail.links[1].address,
        )
        self.assertEqual(
            "metro-2",
            self.region_detail.links[1].label,
        )

    def test_region_detail_state_prices(self):
        self.assertEqual(self.region_detail.prices.state[0], 150)
        self.assertEqual(self.region_detail.prices.state[1], 160)

    def test_region_detail_state_dates(self):
        self.assertEqual(self.region_detail.dates[0], "2023-01")
        self.assertEqual(self.region_detail.dates[1], "2023-02")


class TestRegionDetailMetro(unittest.TestCase):

    def setUp(self) -> None:
        region_detailer = RegionDetailer(data_gateway=RegionDataGatewayMock())
        self.region_detail = region_detailer.get_metro_detail(state_id="1", metro_id="2")

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
            self.region_detail.links[0].address,
            "/state/1/metro/2/city/4",
        )
        self.assertEqual(
            self.region_detail.links[0].label,
            "city-1",
        )
        self.assertEqual(
            self.region_detail.links[1].address,
            f"/state/1/metro/2/city/5",
        )
        self.assertEqual(
            self.region_detail.links[1].label,
            "city-2",
        )

    def test_region_detail_metro_prices(self):
        self.assertEqual(self.region_detail.prices.state[0], 150)
        self.assertEqual(self.region_detail.prices.state[1], 160)

        self.assertEqual(self.region_detail.prices.metro[0], 170)
        self.assertEqual(self.region_detail.prices.metro[1], 180)

    def test_region_detail_metro_dates(self):
        self.assertEqual(self.region_detail.dates[0], "2023-01")
        self.assertEqual(self.region_detail.dates[1], "2023-02")


class TestRegionDetailCity(unittest.TestCase):

    def setUp(self) -> None:
        region_detailer = RegionDetailer(data_gateway=RegionDataGatewayMock())
        self.region_detail = region_detailer.get_city_detail(
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
            self.region_detail.links[0].address,
            "/state/1/metro/2/city/4/neighborhood/6",
        )
        self.assertEqual(
            self.region_detail.links[0].label,
            "neighborhood-1",
        )
        self.assertEqual(
            self.region_detail.links[1].address,
            f"/state/1/metro/2/city/4/neighborhood/7",
        )
        self.assertEqual(
            self.region_detail.links[1].label,
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
        self.assertEqual(self.region_detail.dates[0], "2023-01")
        self.assertEqual(self.region_detail.dates[1], "2023-02")


class TestRegionDetailNeighborhood(unittest.TestCase):

    def setUp(self) -> None:
        region_detailer = RegionDetailer(data_gateway=RegionDataGatewayMock())
        self.region_detail = region_detailer.get_neighborhood_detail(
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
            self.region_detail.links,
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
        self.assertEqual(self.region_detail.dates[0], "2023-01")
        self.assertEqual(self.region_detail.dates[1], "2023-02")


class TestRegionRecords(unittest.TestCase):

    def test_get_breadcrumbs_us(self):
        records = RegionRecords(us=RegionRecord())
        actual_breadcrumbs = records.get_breadcrumbs()
        self.assertEqual("USA", actual_breadcrumbs[0].label)
        self.assertEqual("/", actual_breadcrumbs[0].address)

    def test_get_breadcrumbs_state(self):
        records = RegionRecords(
            us=RegionRecord(),
            state=RegionRecord(region_id="1", region_name="test state"),
        )
        actual_breadcrumbs = records.get_breadcrumbs()
        self.assertEqual("USA", actual_breadcrumbs[0].label)
        self.assertEqual("test state", actual_breadcrumbs[1].label)

        self.assertEqual("/", actual_breadcrumbs[0].address)
        self.assertEqual("/state/1", actual_breadcrumbs[1].address)

    def test_get_breadcrumbs_metro(self):
        records = RegionRecords(
            us=RegionRecord(),
            state=RegionRecord(region_id="1", region_name="test state"),
            metro=RegionRecord(region_id="2", region_name="test metro"),
        )
        actual_breadcrumbs = records.get_breadcrumbs()
        self.assertEqual("USA", actual_breadcrumbs[0].label)
        self.assertEqual("test state", actual_breadcrumbs[1].label)
        self.assertEqual("test metro", actual_breadcrumbs[2].label)

        self.assertEqual("/", actual_breadcrumbs[0].address)
        self.assertEqual("/state/1", actual_breadcrumbs[1].address)
        self.assertEqual("/state/1/metro/2", actual_breadcrumbs[2].address)

    def test_get_breadcrumbs_city(self):
        records = RegionRecords(
            us=RegionRecord(),
            state=RegionRecord(region_id="1", region_name="test state"),
            metro=RegionRecord(region_id="2", region_name="test metro"),
            city=RegionRecord(region_id="3", region_name="test city"),
        )
        actual_breadcrumbs = records.get_breadcrumbs()
        self.assertEqual("USA", actual_breadcrumbs[0].label)
        self.assertEqual("test state", actual_breadcrumbs[1].label)
        self.assertEqual("test metro", actual_breadcrumbs[2].label)
        self.assertEqual("test city", actual_breadcrumbs[3].label)

        self.assertEqual("/", actual_breadcrumbs[0].address)
        self.assertEqual("/state/1", actual_breadcrumbs[1].address)
        self.assertEqual("/state/1/metro/2", actual_breadcrumbs[2].address)
        self.assertEqual("/state/1/metro/2/city/3", actual_breadcrumbs[3].address)

    def test_get_breadcrumbs_neighborhood(self):
        records = RegionRecords(
            us=RegionRecord(),
            state=RegionRecord(region_id="1", region_name="test state"),
            metro=RegionRecord(region_id="2", region_name="test metro"),
            city=RegionRecord(region_id="3", region_name="test city"),
            neighborhood=RegionRecord(region_id="4", region_name="test neighborhood")
        )
        actual_breadcrumbs = records.get_breadcrumbs()
        self.assertEqual("USA", actual_breadcrumbs[0].label)
        self.assertEqual("test state", actual_breadcrumbs[1].label)
        self.assertEqual("test metro", actual_breadcrumbs[2].label)
        self.assertEqual("test city", actual_breadcrumbs[3].label)
        self.assertEqual("test neighborhood", actual_breadcrumbs[4].label)

        self.assertEqual("/", actual_breadcrumbs[0].address)
        self.assertEqual("/state/1", actual_breadcrumbs[1].address)
        self.assertEqual("/state/1/metro/2", actual_breadcrumbs[2].address)
        self.assertEqual("/state/1/metro/2/city/3", actual_breadcrumbs[3].address)
        self.assertEqual("/state/1/metro/2/city/3/neighborhood/4", actual_breadcrumbs[4].address)
