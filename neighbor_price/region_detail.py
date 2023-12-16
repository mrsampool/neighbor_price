from __future__ import annotations
from datetime import datetime
from flask import render_template

from typing import List
from components.zhvi.zhvi_data_gateway import ZhviDataGateway
from components.zhvi.zhvi_record import ZhviRecord
from components.zhvi.zhvi_history_item import ZhviHistoryItem


def prices_from_zhvi_history(history: List[ZhviHistoryItem]) -> List[float]:
    return [history.zhvi_value for history in history]


def dates_from_zhvi_history(history: List[ZhviHistoryItem]) -> List[datetime.datetime]:
    return [history.date for history in history]


class RegionDetail:
    def __init__(
            self,
            zhvi_data_gateway: ZhviDataGateway,
            state_id: str = None,
            metro_id: str = None,
            city_id: str = None,
            neighborhood_id: str = None
    ):
        self.zhvi_data_gateway = zhvi_data_gateway
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
            self.us: ZhviRecord | None = rd.zhvi_data_gateway.get_us_doc()

            self.state: ZhviRecord | None = (
                rd.zhvi_data_gateway.get_region_by_id(region_id=rd.state_id)
            ) if rd.state_id is not None else None

            self.metro: ZhviRecord | None = (
                rd.zhvi_data_gateway.get_region_by_id(region_id=rd.metro_id)
            ) if rd.metro_id is not None else None

            self.city: ZhviRecord | None = (
                rd.zhvi_data_gateway.get_region_by_id(region_id=rd.city_id)
            ) if rd.city_id is not None else None

            self.neighborhood: ZhviRecord | None = (
                rd.zhvi_data_gateway.get_region_by_id(region_id=rd.neighborhood_id)
            ) if rd.neighborhood_id is not None else None

        def get_dates(self):
            if self.neighborhood is not None and len(self.neighborhood.zhvi_history) > 0:
                return dates_from_zhvi_history(self.neighborhood.zhvi_history)

            if self.city is not None and len(self.city.zhvi_history) > 0:
                return dates_from_zhvi_history(self.city.zhvi_history)

            if self.metro is not None and len(self.metro.zhvi_history) > 0:
                return dates_from_zhvi_history(self.metro.zhvi_history)

            if self.state is not None and len(self.state.zhvi_history) > 0:
                return dates_from_zhvi_history(self.state.zhvi_history)

            if self.us is not None and len(self.us.zhvi_history) > 0:
                return dates_from_zhvi_history(self.us.zhvi_history)

    class RegionLinks:
        def __init__(self, rd: RegionDetail):
            if rd.state_id is None:
                state_records: List[ZhviRecord] = rd.zhvi_data_gateway.get_all_states()
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
                    record: ZhviRecord,
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
            self.neighborhood = prices_from_zhvi_history(
                rd.region_records.neighborhood.zhvi_history
            ) if rd.region_records.neighborhood is not None else []

            self.city = prices_from_zhvi_history(
                rd.region_records.city.zhvi_history
            ) if rd.region_records.city is not None else []

            self.metro = prices_from_zhvi_history(
                rd.region_records.metro.zhvi_history
            ) if rd.region_records.metro is not None else []

            self.state = prices_from_zhvi_history(
                rd.region_records.state.zhvi_history
            ) if rd.region_records.state is not None else []

            self.us = prices_from_zhvi_history(
                rd.region_records.us.zhvi_history
            ) if rd.region_records.us is not None else []
