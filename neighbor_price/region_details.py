from dataclasses import dataclass
from datetime import datetime
from typing import List

from components.regions.region_record import RegionRecord
from neighbor_price.region_links import RegionLink, USLink, StateLink, MetroLink, CityLink, NeighborhoodLink


@dataclass
class RegionPrices:
    us: List[float]
    state: List[float] = None
    metro: List[float] = None
    city: List[float] = None
    neighborhood: List[float] = None


@dataclass
class RegionRecords:
    us: RegionRecord
    state: RegionRecord | None = None
    metro: RegionRecord | None = None
    city: RegionRecord | None = None
    neighborhood: RegionRecord | None = None

    def get_prices(self) -> RegionPrices:
        return RegionPrices(
            us=self.us.region_history.get_prices(),
            state=self.state.region_history.get_prices() if self.state is not None else None,
            metro=self.metro.region_history.get_prices() if self.metro is not None else None,
            city=self.city.region_history.get_prices() if self.city is not None else None,
            neighborhood=self.neighborhood.region_history.get_prices() if self.neighborhood is not None else None,
        )

    def get_breadcrumbs(self) -> List[RegionLink]:
        breadcrumbs: List[RegionLink] = []
        if self.us is not None:
            breadcrumbs.append(USLink())
        if self.state is not None:
            breadcrumbs.append(StateLink(
                label=self.state.region_name,
                region_id=self.state.region_id
            ))
        if self.metro is not None:
            breadcrumbs.append(MetroLink(
                label=self.metro.region_name,
                region_id=self.metro.region_id,
                state_id=self.state.region_id
            ))
        if self.city is not None:
            breadcrumbs.append(CityLink(
                label=self.city.region_name,
                region_id=self.city.region_id,
                state_id=self.state.region_id,
                metro_id=self.metro.region_id
            ))
        if self.neighborhood is not None:
            breadcrumbs.append(NeighborhoodLink(
                label=self.neighborhood.region_name,
                region_id=self.neighborhood.region_id,
                state_id=self.state.region_id,
                metro_id=self.metro.region_id,
                city_id=self.city.region_id
            ))
        return breadcrumbs


@dataclass
class RegionDetail:
    region_records: RegionRecords
    links: List[RegionLink]
    prices: RegionPrices
    dates: List[datetime]
    growth_rate: List[datetime]
    breadcrumbs: List[RegionLink]


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
