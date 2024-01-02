#!/usr/bin/env python3
import logging

import pymongo
from typing import List

from components.zhvi.zhvi_record import ZhviRecord, NestedZhviRecord
from components.zhvi.zhvi_history_item import ZhviHistoryItem

DB_COLLECTION_ZHVI_RECORDS = "zvhi_records"

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


class ZhviDataGateway:
    def __init__(self, db_uri: str, db_name: str):
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[DB_COLLECTION_ZHVI_RECORDS]

    def create_zhvi_record(
            self,
            record: ZhviRecord = None,
            region_id: str = 0,
            size_rank: int = 0,
            region_name: str = "",
            region_type: str = "",
            state_name: str = "",
            state: str = "",
            city: str = "",
            metro: str = "",
            county_name: str = "",
            metros: List[NestedZhviRecord] = None,
            cities: List[NestedZhviRecord] = None,
            neighborhods: List[NestedZhviRecord] = None,
            zhvi_history: List[ZhviHistoryItem] = None
    ):
        if zhvi_history is None:
            zhvi_history = []
        if metros is None:
            metros = []
        if cities is None:
            cities = []
        if neighborhods is None:
            neighborhods = []

        if record is None:
            record = ZhviRecord(
                region_id=region_id,
                size_rank=size_rank,
                region_name=region_name,
                region_type=region_type,
                state_name=state_name,
                state=state,
                city=city,
                metro=metro,
                county_name=county_name,
                metros=metros,
                cities=cities,
                neighborhoods=neighborhods,
                zhvi_history=zhvi_history
            )

        doc_history = []
        for item in record.zhvi_history:
            item_doc = {
                "date": item.date,
                "zhvi_value": item.zhvi_value
            }
            doc_history.append(item_doc)

        metros = []
        for metro in record.metros:
            metro_doc = {
                "region_id": metro.region_id,
                "region_name": metro.region_name
            }
            metros.append(metro_doc)

        cities = []
        for city in record.cities:
            city_doc = {
                "region_id": city.region_id,
                "region_name": city.region_name
            }
            cities.append(city_doc)

        neighborhoods = []
        for neighborhood in record.neighborhoods:
            neighborhood_doc = {
                "region_id": neighborhood.region_id,
                "region_name": neighborhood.region_name
            }
            neighborhoods.append(neighborhood_doc)

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
            "metros": metros,
            "cities": cities,
            "neighborhoods": neighborhoods,
            "zhvi_history": doc_history
        }
        self.collection.update_one({"region_id": record.region_id}, {"$set": doc}, True)

    def get_metros_for_state_id(self, state_id: str):
        state_doc = self.collection.find({"region_id"})

    def get_regions_by_type(self, region_type: str):
        return self.collection.find({"region_type": region_type})

    def get_region_by_id(self, region_id) -> ZhviRecord:
        doc = self.collection.find_one({"region_id": region_id})
        return ZhviRecord(document=doc)

    def get_us_doc(self) -> ZhviRecord:
        doc = self.collection.find_one({"region_type": "country", "region_name": "United States"})
        return ZhviRecord(document=doc)

    def get_all_states(self) -> List[ZhviRecord]:
        docs = self.collection.find({"region_type": "state"})
        return list(map(lambda doc: ZhviRecord(document=doc), docs))

    def get_all_metros_for_state_from_name(self, state_name) -> List[ZhviRecord]:
        state_abbrev = get_state_abbrev_from_state_name(state_name)
        docs = self.collection.find({"region_type": "msa", "state_name": state_abbrev})
        return list(map(lambda doc: ZhviRecord(document=doc), docs))

    def get_all_neighborhoods_for_metro_from_name(self, metro_name: str) -> List[ZhviRecord]:
        docs = self.collection.find({"region_type": "neighborhood", "metro": metro_name})
        return list(map(lambda doc: ZhviRecord(document=doc), docs))

    def get_all_cities_for_metro_from_name(self, metro_name):
        docs = self.collection.find({
            "region_type": "city",
            "metro": {"$regex": f"{metro_name}", "$options": "i"}
        })
        return list(map(lambda doc: ZhviRecord(document=doc), docs))

    def get_all_neighborhoods_for_city_from_name(self, city_name):
        docs = self.collection.find({
            "region_type": "neighborhood",
            "city": city_name
        })
        return list(map(lambda doc: ZhviRecord(document=doc), docs))

