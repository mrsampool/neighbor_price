#!/usr/bin/env python3
import logging
import os

import pymongo
from typing import List

from components.regions.region_record import RegionRecord
from components.regions.region_data_gateway import DB_COLLECTION_REGION_RECORDS, get_state_abbrev_from_state_name, \
    RegionDataGateway


class RegionDataGatewayMongo(RegionDataGateway):
    def __init__(self, db_name: str = None, db_uri: str = None, collection=None):
        if collection is not None:
            self.collection = collection
        else:
            client = pymongo.MongoClient(db_uri)
            db = client[db_name]
            self.collection = db[DB_COLLECTION_REGION_RECORDS]

    def save_region_record(self, record: RegionRecord):
        doc_history = []
        for item in record.region_history.history_items:
            item_doc = {
                "date": item.date,
                "region_vale": item.region_value
            }
            doc_history.append(item_doc)

        doc = {
            "region_id": record.region_id,
            "size_rank": record.size_rank,
            "region_name": record.region_name,
            "region_type": record.region_type,
            "state_name": record.state_name,
            "state": record.state,
            "city": record.city,
            "metro": record.metro,
            "county_name": record.county_name,
            "region_history": doc_history
        }
        self.collection.update_one({"region_id": record.region_id}, {"$set": doc}, True)

    def get_region_by_id(self, region_id) -> RegionRecord:
        doc = self.collection.find_one({"region_id": region_id})
        return RegionRecord(document=doc)

    def get_us_record(self) -> RegionRecord:
        doc = self.collection.find_one({"region_type": "country", "region_name": "United States"})
        return RegionRecord(document=doc)

    def get_all_states(self) -> List[RegionRecord]:
        docs = self.collection.find({"region_type": "state"}).sort("name", pymongo.ASCENDING)
        return list(map(lambda doc: RegionRecord(document=doc), docs))

    def get_all_metros_for_state(self, state_name) -> List[RegionRecord]:
        state_abbrev = get_state_abbrev_from_state_name(state_name)
        docs = self.collection.find({
            "region_type": "msa", "state_name": state_abbrev
        }).sort("name", pymongo.ASCENDING)
        return list(map(lambda doc: RegionRecord(document=doc), docs))

    def get_all_cities_for_metro(self, metro_name, state_abbrev):
        metro_without_state_abbrev = metro_name.split(",")[0]
        docs = self.collection.find({
            "region_type": "city",
            "state_name": state_abbrev,
            "metro": {"$regex": f"{metro_without_state_abbrev}", "$options": "i"},
        }).sort("name", pymongo.ASCENDING)
        return list(map(lambda doc: RegionRecord(document=doc), docs))

    def get_all_neighborhoods_for_city(self, city_name: str, state_abbrev: str):
        docs = self.collection.find({
            "region_type": "neighborhood",
            "city": city_name,
            "state": state_abbrev
        }).sort("name", pymongo.ASCENDING)
        return list(map(lambda doc: RegionRecord(document=doc), docs))


class MongoConfig:

    def __init__(
            self,
            db_uri: str | None = None,
            db_name: str | None = None
    ):
        if db_uri is None:
            db_uri = os.getenv("REGION_DB_URI")
            logging.info(f"using REGION_DB_URI: {db_uri}")
            if db_uri is None:
                logging.fatal("Missing required ENV: $REGION_DB_URI")
        self.db_uri = db_uri

        if db_name is None:
            db_name = os.getenv("REGION_DB_NAME")
            logging.info(f"using REGION_DB_NAME: {db_name}")
            if db_name is None:
                logging.fatal("Missing required ENV: $REGION_DB_NAME")
        self.db_name = db_name
