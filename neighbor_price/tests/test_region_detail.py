import unittest
import os
import logging

from components.regions.region_data_gateway import RegionDataGateway
from neighbor_price.region_detail import RegionDetail

class TestRegionDetail(unittest.TestCase):
    def setUp(self) -> None:
        db_uri = os.getenv("REGION_DB_URI")
        logging.info(f"using REGION_DB_URI: {db_uri}")
        if db_uri is None:
            logging.fatal("Missing required ENV: $REGION_DB_URI")

        db_name = os.getenv("REGION_DB_NAME")
        logging.info(f"using REGION_DB_NAME: {db_name}")
        if db_name is None:
            logging.fatal("Missing required ENV: $REGION_DB_NAME")

        self.region_data_gateway = RegionDataGateway(db_uri=db_uri, db_name=db_name)

    def test_region_detail_neighborhood(self):
        self.region_detail = RegionDetail(
            region_data_gateway=self.region_data_gateway,
            state_id="10",
            metro_id="394530",
            neighborhood_id="268743"
        )
        print(self.region_detail)

    def test_region_detail_metro(self):
        self.region_detail = RegionDetail(
            region_data_gateway=self.region_data_gateway,
            state_id="10",
            metro_id="394530",
        )
        print(self.region_detail)

    def test_region_detail_state(self):
        self.region_detail = RegionDetail(
            region_data_gateway=self.region_data_gateway,
            state_id="10",
        )
        print(self.region_detail)
