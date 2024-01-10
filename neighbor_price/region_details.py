from dataclasses import dataclass
from datetime import datetime
from typing import List

from components.regions.region_record import RegionRecord
from neighbor_price.region_links import RegionLink


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
