#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List

from components.regions.region_record import RegionRecord

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


@dataclass
class RegionDataGateway:

    def save_region_record(self, record: RegionRecord):
        raise NotImplementedError

    def get_region_by_id(self, region_id) -> RegionRecord:
        raise NotImplementedError

    def get_us_record(self) -> RegionRecord:
        raise NotImplementedError

    def get_all_states(self) -> List[RegionRecord]:
        raise NotImplementedError

    def get_all_metros_for_state(self, state_name) -> List[RegionRecord]:
        raise NotImplementedError

    def get_all_cities_for_metro(self, metro_name, state_abbrev):
        raise NotImplementedError

    def get_all_neighborhoods_for_city(self, city_name: str, state_abbrev: str):
        raise NotImplementedError
