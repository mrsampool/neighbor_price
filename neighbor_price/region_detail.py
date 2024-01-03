from __future__ import annotations
from datetime import datetime
from flask import render_template

from typing import List
from components.regions.region_data_gateway import RegionDataGateway
from components.regions.region_record import RegionRecord, RegionHistoryItem


def prices_from_region_history(history: List[RegionHistoryItem]) -> List[float]:
    return [history.region_value for history in history]


def dates_from_region_history(history: List[RegionHistoryItem]) -> List[datetime.datetime]:
    return [history.date for history in history]


class RegionDetail:
    def __init__(
            self,
            region_data_gateway: RegionDataGateway,
            state_id: str = None,
            metro_id: str = None,
            city_id: str = None,
            neighborhood_id: str = None
    ):
        self.region_data_gateway = region_data_gateway
        self.state_id = state_id
        self.metro_id = metro_id
        self.city_id = city_id
        self.neighborhood_id = neighborhood_id

        self.region_records = self.RegionRecords(rd=self)
        self.region_links = self.RegionLinks(rd=self)
        self.prices = self.RegionPrices(rd=self)
        self.dates = self.region_records.get_dates()

    class RegionRecords:
        def __init__(self, rd):
            self.us: RegionRecord | None = rd.region_data_gateway.get_us_doc()

            self.state: RegionRecord | None = (
                rd.region_data_gateway.get_region_by_id(region_id=rd.state_id)
            ) if rd.state_id is not None else None

            self.metro: RegionRecord | None = (
                rd.region_data_gateway.get_region_by_id(region_id=rd.metro_id)
            ) if rd.metro_id is not None else None

            self.city: RegionRecord | None = (
                rd.region_data_gateway.get_region_by_id(region_id=rd.city_id)
            ) if rd.city_id is not None else None

            self.neighborhood: RegionRecord | None = (
                rd.region_data_gateway.get_region_by_id(region_id=rd.neighborhood_id)
            ) if rd.neighborhood_id is not None else None

        def get_dates(self):
            if self.neighborhood is not None and len(self.neighborhood.region_history) > 0:
                return dates_from_region_history(self.neighborhood.region_history)

            if self.city is not None and len(self.city.region_history) > 0:
                return dates_from_region_history(self.city.region_history)

            if self.metro is not None and len(self.metro.region_history) > 0:
                return dates_from_region_history(self.metro.region_history)

            if self.state is not None and len(self.state.region_history) > 0:
                return dates_from_region_history(self.state.region_history)

            if self.us is not None and len(self.us.region_history) > 0:
                return dates_from_region_history(self.us.region_history)

    class RegionLinks:
        def __init__(self, rd: RegionDetail):
            if rd.state_id is None:
                state_records: List[RegionRecord] = rd.region_data_gateway.get_all_states()
                self.links = list(map(
                    lambda record: self.RegionLink(record=record, rd=rd, region_type="state"),
                    state_records
                ))

            elif rd.state_id is not None and rd.metro_id is None:
                self.links = list(map(
                    lambda record: self.RegionLink(record=record, rd=rd, region_type="msa"),
                    rd.region_records.state.metros
                ))

            elif rd.metro_id is not None and rd.city_id is None:
                self.links = list(map(
                    lambda record: self.RegionLink(record=record, rd=rd, region_type="city"),
                    rd.region_records.metro.cities
                ))

            elif rd.city_id is not None and rd.neighborhood_id is None:
                self.links = list(map(
                    lambda record: self.RegionLink(record=record, rd=rd, region_type="neighborhood"),
                    rd.region_records.city.neighborhoods
                ))

            else:
                self.links = []

        class RegionLink:
            def __init__(
                    self,
                    record: RegionRecord,
                    rd: RegionDetail,
                    region_type: str
            ):
                self.record = record
                self.label = record.region_name
                self.rd = rd
                self.region_type = region_type
                self.address = self.get_address()

            def get_address(self):
                match self.region_type:
                    case 'state':
                        return f"/state/{self.record.region_id}"
                    case 'msa':
                        return f"/state/{self.rd.state_id}/metro/{self.record.region_id}"
                    case 'city':
                        return f"/state/{self.rd.state_id}/metro/{self.rd.metro_id}/city/{self.record.region_id}"
                    case 'neighborhood':
                        return f"/state/{self.rd.state_id}/metro/{self.rd.metro_id}/city/{self.rd.city_id}/neighborhood/{self.record.region_id}"

    class RegionPrices:
        def __init__(self, rd: RegionDetail):
            self.neighborhood = prices_from_region_history(
                rd.region_records.neighborhood.region_history
            ) if rd.region_records.neighborhood is not None else []

            self.city = prices_from_region_history(
                rd.region_records.city.region_history
            ) if rd.region_records.city is not None else []

            self.metro = prices_from_region_history(
                rd.region_records.metro.region_history
            ) if rd.region_records.metro is not None else []

            self.state = prices_from_region_history(
                rd.region_records.state.region_history
            ) if rd.region_records.state is not None else []

            self.us = prices_from_region_history(
                rd.region_records.us.region_history
            ) if rd.region_records.us is not None else []
