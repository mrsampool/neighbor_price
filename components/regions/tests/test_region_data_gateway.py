import datetime
import unittest
from components.regions.region_data_gateway_mock import (
    RegionDataGatewayMock
)
from components.regions.region_record import RegionRecord, RegionHistoryItem, RegionHistory


class TestRegionNeighborhoodDataGateway(unittest.TestCase):

    def setUp(self) -> None:
        self.gateway = RegionDataGatewayMock()

    def drop_and_seed_documents(self, documents):
        self.collection.drop()
        self.collection.insert_many(documents)

    def test_save_neighborhood_record(self):
        self.collection.drop()
        record = RegionRecord(
            region_id="1",
            size_rank=1,
            region_name="test_region_name",
            region_type="test_region_type",
            state_name="test_state_name",
            state="test_state",
            city="test_city",
            metro="test_metro",
            county_name="test_county_name",
            region_history=RegionHistory(
                items=[
                    RegionHistoryItem(
                        date=datetime.datetime(year=2000, month=1, day=31),
                        region_value=75553.2814897809
                    ),
                    RegionHistoryItem(
                        date=datetime.datetime(year=2000, month=2, day=29),
                        region_value=75756.46950997740
                    ),
                ]
            )
        )
        self.gateway.save_region_record(record)

        documents = self.collection.find()
        actual_document = documents[0]

        self.assertEqual(actual_document["region_id"], "1")
        self.assertEqual(actual_document["size_rank"], 1)
        self.assertEqual(actual_document["region_name"], "test_region_name")
        self.assertEqual(actual_document["region_type"], "test_region_type")
        self.assertEqual(actual_document["state_name"], "test_state_name")
        self.assertEqual(actual_document["state"], "test_state")
        self.assertEqual(actual_document["city"], "test_city")
        self.assertEqual(actual_document["metro"], "test_metro")
        self.assertEqual(actual_document["county_name"], "test_county_name")

        actual_history_1 = actual_document["region_history"][0]
        self.assertEqual(datetime.date.isoformat(actual_history_1["date"]), "2000-01-31")
        self.assertEqual(actual_history_1["region_vale"], 75553.2814897809)

        actual_history_2 = actual_document["region_history"][1]
        self.assertEqual(datetime.date.isoformat(actual_history_2["date"]), "2000-02-29")
        self.assertEqual(actual_history_2["region_vale"], 75756.46950997740)

    def test_get_region_by_id(self):
        self.drop_and_seed_documents([
            {
                "region_id": "1",
                "region_name": "test-region-1",
            },
            {
                "region_id": "2",
                "region_name": "test-region-2",
            },
        ])
        actual = self.gateway.get_region_by_id("1")
        self.assertEqual(actual.region_name, "test-region-1")

    def test_get_us_doc(self):
        self.drop_and_seed_documents([
            {
                "region_type": "country",
                "region_name": "United States",
                "size_rank": "test-size-rank"
            },
        ])
        actual = self.gateway.get_us_record()
        self.assertEqual(actual.size_rank, "test-size-rank")

    def test_get_all_states(self):
        self.drop_and_seed_documents([
            {
                "region_type": "state",
                "region_name": "test-state-1",
            },
            {
                "region_type": "state",
                "region_name": "test-state-2",
            },
            {
                "region_type": "state",
                "region_name": "test-state-3",
            },
            {
                "region_type": "city",
                "region_name": "test-city-1",
            },
        ])
        actual_records = self.gateway.get_all_states()

        self.assertEqual(3, len(actual_records))

        actual_names = {record.region_name for record in actual_records}
        expected_names = ["test-state-1", "test-state-2", "test-state-3"]
        self.assertTrue(all(name in actual_names for name in expected_names))

    def test_get_all_metros_for_state(self):
        self.drop_and_seed_documents([
            {
                "region_type": "msa",
                "region_name": "test-msa-1",
                "state_name": "AL"
            },
            {
                "region_type": "msa",
                "region_name": "test-msa-2",
                "state_name": "AL"
            },
            {
                "region_type": "msa",
                "region_name": "test-msa-3",
                "state_name": "TX"
            },
        ])
        actual_records = self.gateway.get_all_metros_for_state(state_name="Alaska")

        self.assertEqual(2, len(actual_records))

        actual_names = {record.region_name for record in actual_records}
        expected_names = ["test-msa-1", "test-msa-2"]
        self.assertTrue(all(name in actual_names for name in expected_names))

    def test_get_all_cities_for_metro(self):
        self.drop_and_seed_documents([
            {
                "region_type": "city",
                "state_name": "CO",
                "metro": "city1-city2-msa",
                "region_name": "city1"
            },
            {
                "region_type": "city",
                "state_name": "CO",
                "metro": "city1-city2-msa",
                "region_name": "city2"
            },
            {
                "region_type": "city",
                "state_name": "CO",
                "metro": "city3-city4-msa",
                "region_name": "city3"
            },
            {
                "region_type": "city",
                "state_name": "NM",
                "metro": "city1-city2-msa",
                "region_name": "city2"
            },
            {
                "region_type": "state",
                "state_name": "",
                "metro": "",
                "region_name": "CO"
            },

        ])
        actual_records = self.gateway.get_all_cities_for_metro(
            metro_name="city1",
            state_abbrev="CO"
        )

        self.assertEqual(2, len(actual_records))

        actual_names = {record.region_name for record in actual_records}
        expected_names = ["city1", "city2"]
        self.assertTrue(all(name in actual_names for name in expected_names))

    def test_get_all_neighborhoods_for_city(self):
        self.drop_and_seed_documents([
            {
                "region_type": "neighborhood",
                "region_name": "neighborhood1",
                "city": "city1",
                "state": "CO"
            },
            {
                "region_type": "neighborhood",
                "region_name": "neighborhood2",
                "city": "city1",
                "state": "CO"
            },
            {
                "region_type": "neighborhood",
                "region_name": "neighborhood3",
                "city": "city2",
                "state": "CO"
            },
            {
                "region_type": "neighborhood",
                "region_name": "neighborhood4",
                "city": "city1",
                "state": "NM"
            },
        ])
        actual_records = self.gateway.get_all_neighborhoods_for_city(
            city_name="city1",
            state_abbrev="CO"
        )

        self.assertEqual(2, len(actual_records))

        actual_names = {record.region_name for record in actual_records}
        expected_names = ["neighborhood1", "neighborhood2"]
        self.assertTrue(all(name in actual_names for name in expected_names))
