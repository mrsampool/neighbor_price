from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass

from typing import List
from components.regions.region_data_gateway import RegionDataGateway
from components.regions.region_record import RegionRecord


@dataclass
class RegionRecords:
    us: RegionRecord | None = None
    state: RegionRecord | None = None
    metro: RegionRecord | None = None
    city: RegionRecord | None = None
    neighborhood: RegionRecord | None = None


@dataclass
class RegionPrices:
    us: List[float]
    state: List[float] = None
    metro: List[float] = None
    city: List[float] = None
    neighborhood: List[float] = None


class RegionLink:
    def __init__(
            self,
            label: str,
            region_type: str,
            region_id: str,
            state_id: str | None,
            metro_id: str | None,
            city_id: str | None,
    ):
        self.label = label
        self.region_type: str = region_type
        self.region_id: str = region_id
        self.state_id: str = state_id
        self.metro_id: str = metro_id
        self.city_id: str = city_id
        self.address: str = self.get_address()

    def get_address(self):
        match self.region_type:
            case 'state':
                return f"/state/{self.region_id}"
            case 'msa':
                return f"/state/{self.state_id}/metro/{self.region_id}"
            case 'city':
                return f"/state/{self.state_id}/metro/{self.metro_id}/city/{self.region_id}"
            case 'neighborhood':
                return f"/state/{self.state_id}/metro/{self.metro_id}/city/{self.city_id}/neighborhood/{self.region_id}"


@dataclass
class RegionRecords:
    us: RegionRecord
    state: RegionRecord
    metro: RegionRecord
    city: RegionRecord
    neighborhood: RegionRecord


@dataclass
class RegionDetail:
    region_records: RegionRecords
    links: List[RegionLink]
    prices: RegionPrices
    dates: List[datetime]


@dataclass
class StateDetail(RegionDetail):
    state_id: str


@dataclass
class MetroDetail(RegionDetail):
    state_id: str
    metro_id: str


@dataclass
class CityDetail(RegionDetail):
    state_id: str
    metro_id: str
    metro_id: str
    city_id: str


@dataclass
class NeighborhoodDetail(RegionDetail):
    state_id: str
    metro_id: str
    metro_id: str
    city_id: str


def build_links_for_records(
        region_type: str | None,
        records: List[RegionRecord],
        state_id: str = None,
        metro_id: str = None,
        city_id: str = None
) -> List[RegionLink]:
    return list(map(
        lambda record: RegionLink(
            region_type=region_type,
            region_id=record.region_id,
            label=record.region_name,
            state_id=state_id,
            metro_id=metro_id,
            city_id=city_id
        ),
        records
    ))


@dataclass
class RegionDetailer:
    data_gateway: RegionDataGateway

    def get_us_detail(self) -> RegionDetail:
        us_record = self.data_gateway.get_us_record()
        state_records = self.data_gateway.get_all_states()
        return RegionDetail(
            region_records=RegionRecords(
                us=us_record,
                state=None,
                metro=None,
                city=None,
                neighborhood=None
            ),
            links=build_links_for_records(
                region_type="state",
                records=state_records
            ),
            prices=RegionPrices(us=us_record.region_history.get_prices()),
            dates=us_record.region_history.get_dates()
        )

    def get_state_detail(self, state_id) -> RegionDetail:
        us_record = self.data_gateway.get_us_record()
        state_record = self.data_gateway.get_region_by_id(region_id=state_id)
        metro_records = self.data_gateway.get_all_metros_for_state(state_name=state_record.region_name)
        return RegionDetail(
            region_records=RegionRecords(
                us=us_record,
                state=state_record,
                metro=None,
                city=None,
                neighborhood=None
            ),
            links=build_links_for_records(
                region_type="state",
                records=metro_records
            ),
            prices=RegionPrices(
                us=us_record.region_history.get_prices(),
                state=state_record.region_history.get_prices()
            ),
            dates=us_record.region_history.get_dates()
        )

    """

    def get_state_detail(self, state_id: str) -> StateDetail:

    def get_city_detail(
            self,
            city_id: str,
            state_id: str
    ) -> CityDetail:

    def get_metro_detail(
            self,
            metro_id: str,
            city_id: str,
            state_id: str
    ) -> MetroDetail:

    def get_neighborhood_detail(
            self,
            neighborhood_id: str,
            city_id: str,
            metro_id: str,
            state_id: str
    ) -> NeighborhoodDetail:
    """


"""
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
                self.links = list(map(
                    lambda record: self.RegionLink(record=record, rd=rd, region_type="state"),
                    rd.region_data_gateway.get_all_states()
                ))

            elif rd.state_id is not None and rd.metro_id is None:
                self.links = list(map(
                    lambda record: self.RegionLink(record=record, rd=rd, region_type="msa"),
                    rd.region_data_gateway.get_all_metros_for_state(state_name=rd.region_records.state.region_name)
                ))

            elif rd.metro_id is not None and rd.city_id is None:
                self.links = list(map(
                    lambda record: self.RegionLink(record=record, rd=rd, region_type="city"),
                    rd.region_data_gateway.get_all_cities_for_metro(
                        metro_name=rd.region_records.metro.region_name,
                        state_abbrev=rd.region_records.metro.state_name
                    )
                ))

            elif rd.city_id is not None and rd.neighborhood_id is None:
                self.links = list(map(
                    lambda record: self.RegionLink(record=record, rd=rd, region_type="neighborhood"),
                    rd.region_data_gateway.get_all_neighborhoods_for_city(
                        city_name=rd.region_records.city.region_name,
                        state_abbrev=rd.region_records.city.state_name
                    )
                ))

            else:
                self.links = []



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
"""
