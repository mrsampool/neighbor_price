import datetime
import logging
import os

import pymongo
import pytest

from components.regions.region_data_gateway import DB_COLLECTION_REGION_RECORDS
from components.regions.region_data_gateway_mongo import MongoConfig, RegionDataGatewayMongo
from components.regions.region_record import RegionRecord, RegionHistoryItem, RegionHistory
from neighbor_price.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client



@pytest.fixture
def collection():
    mongo_config = MongoConfig()

    region_data_gateway = RegionDataGatewayMongo(db_name=mongo_config.db_name, db_uri=mongo_config.db_uri)

    region_data_gateway.save_region_record(
        RegionRecord(
            region_name="United States",
            region_type="country",
            size_rank=0,
            region_id="102001",
            region_history=RegionHistory(items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 31),
                    region_value=100
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 29),
                    region_value=200
                )
            ])
        )
    )
    region_data_gateway.save_region_record(
        RegionRecord(
            region_name="California",
            region_type="state",
            size_rank=1,
            region_id="9",
            region_history=RegionHistory(items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 31),
                    region_value=101
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 29),
                    region_value=201
                )
            ])
        )
    )
    region_data_gateway.save_region_record(
        RegionRecord(
            region_name="Texas",
            region_type="state",
            size_rank=1,
            region_id="54",
            region_history=RegionHistory(items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 31),
                    region_value=97511.5147086164
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 29),
                    region_value=97568.22178801979
                )
            ])
        )
    )
    region_data_gateway.save_region_record(
        RegionRecord(
            region_name="Los Angeles, CA",
            region_type="msa",
            size_rank=2,
            region_id="753899",
            state_name="CA",
            region_history=RegionHistory(items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 31),
                    region_value=207432.60302071064
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 29),
                    region_value=208152.50626904995
                )
            ])
        )
    )
    region_data_gateway.save_region_record(
        RegionRecord(
            region_name="San Francisco, CA",
            region_type="msa",
            size_rank=12,
            region_id="395057",
            state_name="CA",
            region_history=RegionHistory(items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 31),
                    region_value=207432.60302071064
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 29),
                    region_value=208152.50626904995
                )
            ])
        )
    )
    region_data_gateway.save_region_record(
        RegionRecord(
            region_name="San Francisco",
            region_type="city",
            size_rank=17,
            region_id="20330",
            state_name="CA",
            state="CA",
            metro="San Francisco-Oakland-Berkeley, CA",
            region_history=RegionHistory(items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 31),
                    region_value=207432.60302071064
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 29),
                    region_value=208152.50626904995
                )
            ])
        )
    )
    region_data_gateway.save_region_record(
        RegionRecord(
            region_name="Oakland",
            region_type="city",
            size_rank=51,
            region_id="13072",
            state_name="CA",
            state="CA",
            metro="San Francisco-Oakland-Berkeley, CA",
            region_history=RegionHistory(items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 31),
                    region_value=207432.60302071064
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 29),
                    region_value=208152.50626904995
                )
            ])
        )
    )
    region_data_gateway.save_region_record(
        RegionRecord(
            region_name="Russian Hill",
            region_type="neighborhood",
            size_rank=51,
            region_id="268450",
            state_name="CA",
            state="CA",
            metro="San Francisco-Oakland-Berkeley, CA",
            city="San Francisco",
            region_history=RegionHistory(items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 31),
                    region_value=207432.60302071064
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 29),
                    region_value=208152.50626904995
                )
            ])
        )
    )
    region_data_gateway.save_region_record(
        RegionRecord(
            region_name="Nob Hill",
            region_type="neighborhood",
            size_rank=51,
            region_id="268337",
            state_name="CA",
            state="CA",
            metro="San Francisco-Oakland-Berkeley, CA",
            city="San Francisco",
            region_history=RegionHistory(items=[
                RegionHistoryItem(
                    date=datetime.datetime(2000, 1, 31),
                    region_value=207432.60302071064
                ),
                RegionHistoryItem(
                    date=datetime.datetime(2000, 2, 29),
                    region_value=208152.50626904995
                )
            ])
        )
    )

    yield collection
