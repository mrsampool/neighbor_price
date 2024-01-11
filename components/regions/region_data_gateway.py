#!/usr/bin/env python3
import logging

import pymongo
from typing import List

from components.regions.region_record import RegionRecord, NestedRegionRecord, RegionHistory

DB_COLLECTION_REGION_RECORDS = "region_records"

state_names_and_abbrev = [
    {"abbrev": "AL", "name": "Alaska"},
    {"abbrev": "AZ", "name": "Arizona"},
    {"abbrev": "AR", "name": "Arkansas"},
    {"abbrev": "AL", "name": "Alabama"},
    {"abbrev": "CA", "name": "California"},
    {"abbrev": "CO", "name": "Colorado"},
    {"abbrev": "DE", "name": "Delaware"},
    {"abbrev": "DC", "name": "District of Columbia"},
    {"abbrev": "CT", "name": "Connecticut"},
    {"abbrev": "FL", "name": "Florida"},
    {"abbrev": "GA", "name": "Georgia"},
    {"abbrev": "HI", "name": "Hawaii"},
    {"abbrev": "IA", "name": "Iowa"},
    {"abbrev": "ID", "name": "Idaho"},
    {"abbrev": "IL", "name": "Illinois"},
    {"abbrev": "IN", "name": "Indiana"},
    {"abbrev": "KS", "name": "Kansas"},
    {"abbrev": "KY", "name": "Kentucky"},
    {"abbrev": "LA", "name": "Louisiana"},
    {"abbrev": "MA", "name": "Massachusetts"},
    {"abbrev": "MD", "name": "Maryland"},
    {"abbrev": "MI", "name": "Michigan"},
    {"abbrev": "MS", "name": "Mississippi"},
    {"abbrev": "MO", "name": "Missouri"},
    {"abbrev": "MN", "name": "Minnesota"},
    {"abbrev": "MO", "name": "Montana"},
    {"abbrev": "NC", "name": "North Carolina"},
    {"abbrev": "ND", "name": "North Dakota"},
    {"abbrev": "NE", "name": "Nebraska"},
    {"abbrev": "NV", "name": "Nevada"},
    {"abbrev": "NH", "name": "New Hampshire"},
    {"abbrev": "NJ", "name": "New Jersey"},
    {"abbrev": "NM", "name": "New Mexico"},
    {"abbrev": "NY", "name": "New York"},
    {"abbrev": "ME", "name": "Maine"},
    {"abbrev": "OH", "name": "Ohio"},
    {"abbrev": "OR", "name": "Oregon"},
    {"abbrev": "OK", "name": "Oklahoma"},
    {"abbrev": "RI", "name": "Rhode Island"},
    {"abbrev": "PN", "name": "Pennsylvania"},
    {"abbrev": "SC", "name": "South Carolina"},
    {"abbrev": "SD", "name": "South Dakota"},
    {"abbrev": "TN", "name": "Tennessee"},
    {"abbrev": "TX", "name": "Texas"},
    {"abbrev": "UT", "name": "Utah"},
    {"abbrev": "WA", "name": "Washington"},
    {"abbrev": "WV", "name": "West Virginia"},
    {"abbrev": "WY", "name": "Wyoming"},
    {"abbrev": "WI", "name": "Wisonsin"},
    {"abbrev": "VA", "name": "Virginia"},
    {"abbrev": "VT", "name": "Vermont"},
]


def get_state_name_from_state_abbrev(state_abbrev: str) -> str:
    return next((state["name"] for state in state_names_and_abbrev if state["abbrev"] == state_abbrev), None)


def get_state_abbrev_from_state_name(state_name: str) -> str:
    return next((state["abbrev"] for state in state_names_and_abbrev if state["name"] == state_name), None)


class RegionDataGateway:
    def __init__(self, db_name: str = None, db_uri: str = None, collection=None):
        if collection is None:
            client = pymongo.MongoClient(db_uri)
            db = client[db_name]
            self.collection = db[DB_COLLECTION_REGION_RECORDS]
        else:
            self.collection = collection

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
        docs = self.collection.find({"region_type": "state"})
        return list(map(lambda doc: RegionRecord(document=doc), docs))

    def get_all_metros_for_state(self, state_name) -> List[RegionRecord]:
        state_abbrev = get_state_abbrev_from_state_name(state_name)
        docs = self.collection.find({"region_type": "msa", "state_name": state_abbrev})
        return list(map(lambda doc: RegionRecord(document=doc), docs))

    def get_all_cities_for_metro(self, metro_name, state_abbrev):
        docs = self.collection.find({
            "region_type": "city",
            "state_name": state_abbrev,
            "metro": {"$regex": f"{metro_name}", "$options": "i"},
        })
        return list(map(lambda doc: RegionRecord(document=doc), docs))

    def get_all_neighborhoods_for_city(self, city_name: str, state_abbrev: str):
        docs = self.collection.find({
            "region_type": "neighborhood",
            "city": city_name,
            "state": state_abbrev
        })
        return list(map(lambda doc: RegionRecord(document=doc), docs))

