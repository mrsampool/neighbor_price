import unittest
import logging
import os
from flask import Flask
from src.components.zillow_neighborhoods.zhvi_neighborhood_data_gateway import ZhviNeighborhoodDataGateway
from src.components.zillow_neighborhoods.zhvi_neighborhood_record import ZhviNeighborhoodRecord, db


class TestZhviNeighborhoodDataGateway(unittest.TestCase):

    def setUp(self) -> None:
        db_uri = os.getenv("TEST_ZHVI_DB_URI")
        if db_uri is None or db_uri == "":
            logging.fatal("Missing required ENV: $TEST_ZHVI_DB_URI")

        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

        self.gateway = ZhviNeighborhoodDataGateway(app=self.app)
        with self.app.app_context():
            db.session.execute(db.delete(ZhviNeighborhoodRecord))
            db.session.commit()

    def test_create_neighborhoods_from_df(self):
        record = ZhviNeighborhoodRecord(
            region_id=1,
            size_rank=1,
            region_name="test_region_name",
            region_type="test_region_type",
            state_name="test_state_name",
            state="test_state",
            city="test_city",
            metro="test_metro",
            county_name="test_county_name",
        )
        self.gateway.create_neighborhood_record(record)

        with self.app.app_context():
            result = db.session.execute(db.select(ZhviNeighborhoodRecord))
            for row in result.scalars():
                record = row

        self.assertEqual(record.region_id, 1)
        self.assertEqual(record.size_rank, 1)
        self.assertEqual(record.region_name, "test_region_name")
        self.assertEqual(record.region_type, "test_region_type")
        self.assertEqual(record.state_name, "test_state_name")
        self.assertEqual(record.state, "test_state")
        self.assertEqual(record.city, "test_city")
        self.assertEqual(record.metro, "test_metro")
        self.assertEqual(record.county_name, "test_county_name")
