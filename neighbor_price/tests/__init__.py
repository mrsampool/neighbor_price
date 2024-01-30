import logging
import os

import pymongo
import pytest

from components.regions.region_data_gateway import DB_COLLECTION_REGION_RECORDS
from neighbor_price.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client



@pytest.fixture
def collection():
    db_uri = os.getenv("REGION_DB_URI")
    logging.info(f"using REGION_DB_URI: {db_uri}")
    if db_uri is None:
        logging.fatal("Missing required ENV: $REGION_DB_URI")

    db_name = os.getenv("REGION_DB_NAME")
    logging.info(f"using REGION_DB_NAME: {db_name}")
    if db_name is None:
        logging.fatal("Missing required ENV: $REGION_DB_NAME")

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[DB_COLLECTION_REGION_RECORDS]

    collection.drop()
    collection.insert_many([
        {
            "region_id": "102001",
            "region_history": [
                {
                    "date": {
                        "$date": "2000-01-31T00:00:00.000Z"
                    },
                    "region_vale": 100
                },
                {
                    "date": {
                        "$date": "2000-02-29T00:00:00.000Z"
                    },
                    "region_vale": 200
                },
            ],
            "region_name": "United States",
            "region_type": "country",
            "size_rank": "0",
        },
        {
            "region_id": "9",
            "region_history": [
                {
                    "date": {
                        "$date": "2000-01-31T00:00:00.000Z"
                    },
                    "region_vale": 101
                },
                {
                    "date": {
                        "$date": "2000-02-29T00:00:00.000Z"
                    },
                    "region_vale": 201
                },
            ],
            "region_name": "California",
            "region_type": "state",
            "size_rank": "0",
        }
    ])

    yield collection
