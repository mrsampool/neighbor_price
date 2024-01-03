import logging
from typing import List
from datetime import datetime


class RegionHistoryItem:
    def __init__(self, date: datetime, region_vale: float):
        self.date: datetime = date
        self.region_value: float = region_vale


class NestedRegionRecord:
    def __init__(self, region_id: str, region_name: str):
        self.region_id = region_id
        self.region_name = region_name


def parse_region_history_from_doc(doc_history) -> List[RegionHistoryItem]:
    history = []
    if doc_history is not None:
        for history_item in doc_history:
            history.append(
                RegionHistoryItem(
                    date=history_item["date"],
                    region_vale=float(history_item["region_value"])
                )
            )
    return history


def parse_nested_region_records_from_doc(doc_records) -> List[NestedRegionRecord]:
    records = []
    if doc_records is not None:
        for record in doc_records:
            records.append(
                NestedRegionRecord(
                    region_id=record.get("region_id"),
                    region_name=record.get("region_name")
                )
            )
    return records


class RegionRecord:
    def __init__(
            self,
            document=None,
            pd_series=None,
            region_id: str = None,
            size_rank: int = None,
            region_name: str = None,
            region_type: str = None,
            state_name: str = None,
            state: str = None,
            city: str = None,
            metro: str = None,
            county_name: str = None,
            metros: List[NestedRegionRecord] = [],
            cities: List[NestedRegionRecord] = [],
            neighborhoods: List[NestedRegionRecord] = [],
            region_history: List[RegionHistoryItem] = [],
    ):
        if document is not None:
            self.init_from_document(document=document)

        elif pd_series is not None:
            self.init_from_pd_series(pd_series=pd_series)

        else:
            self.region_id: str = region_id
            self.size_rank: int = size_rank
            self.region_name: str = region_name
            self.region_type: str = region_type
            self.state_name: str = state_name
            self.state: str = state
            self.city: str = city
            self.metro: str = metro
            self.county_name: str = county_name
            self.region_history: List[RegionHistoryItem] = region_history
            self.metros: List[NestedRegionRecord] = metros
            self.cities: List[NestedRegionRecord] = cities
            self.neighborhoods: List[NestedRegionRecord] = neighborhoods

    def init_from_document(self, document):
        self.region_id: int = document.get("region_id")
        self.size_rank: int = document.get("size_rank")
        self.region_name: str = document.get("region_name")
        self.region_type: str = document.get("region_type")
        self.state_name: str = document.get("state_name")
        self.state: str = document.get("state")
        self.city: str = document.get("city")
        self.metro: str = document.get("metro")
        self.county_name: str = document.get("county_name")
        self.region_history = []
        self.region_history = parse_region_history_from_doc(document.get("region_history"))
        self.metros = parse_nested_region_records_from_doc(document.get("metros"))
        self.cities = parse_nested_region_records_from_doc(document.get("cities"))
        self.neighborhoods = parse_nested_region_records_from_doc(document.get("neighborhoods"))

    def init_from_pd_series(self, pd_series):
        self.region_id: int = pd_series.loc['RegionID'].iloc[0]
        self.size_rank: int = pd_series.loc['SizeRank'].iloc[0]
        self.region_name: str = pd_series.loc['RegionName'].iloc[0]
        self.region_type: str = pd_series.loc['RegionType'].iloc[0]
        self.state_name: str = pd_series.loc['StateName'].iloc[0]
        self.metros: List[NestedRegionRecord] = []
        self.cities: List[NestedRegionRecord] = []
        self.neighborhoods: List[NestedRegionRecord] = []

        cols = pd_series.index.values

        if 'State' in cols:
            self.state: str = pd_series.loc['State'].iloc[0]
        else:
            self.state = None

        if 'City' in cols:
            self.city: str = pd_series.loc['City'].iloc[0]
        else:
            self.city = None

        if 'Metro' in cols:
            self.metro = pd_series.loc['Metro'].iloc[0]
        else:
            self.metro = None

        if 'CountyName' in cols:
            self.county_name: str = pd_series.loc['CountyName'].iloc[0]
        else:
            self.county_name = None

        region_history = []

        history_start_index = pd_series.index.get_loc('2000-01-31')
        region_history_df = pd_series.iloc[history_start_index:]
        for date, region_value in region_history_df.iterrows():
            if region_value.iloc[0] is not None and region_value.iloc[0] != "":
                region_history.append(
                    RegionHistoryItem(
                        date=datetime.strptime(date, '%Y-%m-%d'),
                        region_vale=float(region_value.iloc[0])
                    )
                )
        self.region_history = region_history

