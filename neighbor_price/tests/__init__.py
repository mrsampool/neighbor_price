import logging
import os

import pymongo
import pytest

from components.regions.region_data_gateway import DB_COLLECTION_REGION_RECORDS
from components.regions.region_data_gateway_mongo import MongoConfig
from neighbor_price.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client



@pytest.fixture
def collection():
    mongo_config = MongoConfig()

    client = pymongo.MongoClient(mongo_config.db_uri)
    db = client[mongo_config.db_name]
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
        },
        {
            "region_id": "54",
            "region_history": [
                {
                    "date": {
                        "$date": "2000-01-31T00:00:00.000Z"
                    },
                    "region_vale": 97511.5147086164
                },
                {
                    "date": {
                        "$date": "2000-02-29T00:00:00.000Z"
                    },
                    "region_vale": 97568.22178801979
                },
            ],
            "region_name": "Texas",
            "region_type": "state",
            "size_rank": "1",
        },
        {
            "region_id": "753899",
            "region_history": [
                {
                    "date": {
                        "$date": "2000-01-31T00:00:00.000Z"
                    },
                    "region_vale": 207432.60302071064
                },
                {
                    "date": {
                        "$date": "2000-02-29T00:00:00.000Z"
                    },
                    "region_vale": 208152.50626904995
                },
            ],
            "region_name": "Los Angeles, CA",
            "region_type": "msa",
            "size_rank": "2",
            "state_name": "CA"
        },
        {
            "region_id": "395057",
            "region_history": [
                {
                    "date": {
                        "$date": "2000-01-31T00:00:00.000Z"
                    },
                    "region_vale": 266017.4373916068
                },
                {
                    "date": {
                        "$date": "2000-02-29T00:00:00.000Z"
                    },
                    "region_vale": 267065.88090566616
                },
            ],
            "region_name": "San Francisco, CA",
            "region_type": "msa",
            "size_rank": "12",
            "state_name": "CA"
        },
        {
            "region_id": "20330",
            "county_name": "San Francisco County",
            "metro": "San Francisco-Oakland-Berkeley, CA",
            "region_history": [
                {
                    "date": {
                        "$date": "2000-01-31T00:00:00.000Z"
                    },
                    "region_vale": 398003.91540533473
                },
                {
                    "date": {
                        "$date": "2000-02-29T00:00:00.000Z"
                    },
                    "region_vale": 400032.6355934929
                },
            ],
            "region_name": "San Francisco",
            "region_type": "city",
            "size_rank": "17",
            "state": "CA",
            "state_name": "CA"
        },
        {
            "region_id": "13072",
            "county_name": "Alameda County",
            "metro": "San Francisco-Oakland-Berkeley, CA",
            "region_history": [
                {
                    "date": {
                        "$date": "2000-01-31T00:00:00.000Z"
                    },
                    "region_vale": 190878.24185273724
                },
                {
                    "date": {
                        "$date": "2000-02-29T00:00:00.000Z"
                    },
                    "region_vale": 191480.05035176766
                }
            ],
            "region_name": "Oakland",
            "region_type": "city",
            "size_rank": "51",
            "state": "CA",
            "state_name": "CA"
        },
        {
            "region_id": "268450",
            "city": "San Francisco",
            "county_name": "San Francisco County",
            "metro": "San Francisco-Oakland-Berkeley, CA",
            "region_history": [
                {
                    "date": {
                        "$date": "2000-01-31T00:00:00.000Z"
                    },
                    "region_vale": 1210968.8808659264
                },
                {
                    "date": {
                        "$date": "2000-02-29T00:00:00.000Z"
                    },
                    "region_vale": 1220989.6052692079
                },
            ],
            "region_name": "Russian Hill",
            "region_type": "neighborhood",
            "size_rank": "1153",
            "state": "CA",
            "state_name": "CA"
        },
        {
            "region_id": "268337",
            "city": "San Francisco",
            "county_name": "San Francisco County",
            "metro": "San Francisco-Oakland-Berkeley, CA",
            "region_history": [
                {
                    "date": {
                        "$date": "2000-01-31T00:00:00.000Z"
                    },
                    "region_vale": 752384.0413282032
                },
                {
                    "date": {
                        "$date": "2000-02-29T00:00:00.000Z"
                    },
                    "region_vale": 755852.5164959942
                }
            ],
            "region_name": "Nob Hill",
            "region_type": "neighborhood",
            "size_rank": "1126",
            "state": "CA",
            "state_name": "CA"
        }
    ])

    yield collection
