import logging
from typing import List
from datetime import datetime

from components.zhvi.zhvi_history_item import ZhviHistoryItem


class NestedZhviRecord:
    def __init__(self, region_id: str, region_name: str):
        self.region_id = region_id
        self.region_name = region_name


class ZhviRecord:
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
            metros: List[NestedZhviRecord] = [],
            cities: List[NestedZhviRecord] = [],
            neighborhoods: List[NestedZhviRecord] = [],
            zhvi_history: List[ZhviHistoryItem] = [],
    ):
        if document is not None:
            self.region_id: int = document["region_id"]
            self.size_rank: int = document["size_rank"]
            self.region_name: str = document["region_name"]
            self.region_type: str = document["region_type"]
            self.state_name: str = document["state_name"]
            self.state: str = document["state"]
            self.city: str = document["city"]
            self.metro: str = document["metro"]
            self.county_name: str = document["county_name"]
            self.zhvi_history = []
            for history_item in document["zhvi_history"]:
                self.zhvi_history.append(
                    ZhviHistoryItem(
                        date=history_item["date"],
                        zhvi_value=float(history_item["zhvi_value"])
                    )
                )
            self.metros = []
            for metro in document["metros"]:
                self.metros.append(
                    NestedZhviRecord(
                        region_id=metro["region_id"],
                        region_name=metro["region_name"]
                    )
                )
            self.cities = []
            for city in document["cities"]:
                self.cities.append(
                    NestedZhviRecord(
                        region_id=city["region_id"],
                        region_name=city["region_name"]
                    )
                )
            self.neighborhoods = []
            for neighborhood in document["neighborhoods"]:
                self.neighborhoods.append(
                    NestedZhviRecord(
                        region_id=neighborhood["region_id"],
                        region_name=neighborhood["region_name"]
                    )
                )

        elif pd_series is not None:
            self.region_id: int = pd_series.loc['RegionID'].iloc[0]
            self.size_rank: int = pd_series.loc['SizeRank'].iloc[0]
            self.region_name: str = pd_series.loc['RegionName'].iloc[0]
            self.region_type: str = pd_series.loc['RegionType'].iloc[0]
            self.state_name: str = pd_series.loc['StateName'].iloc[0]
            self.metros: List[NestedZhviRecord] = []
            self.cities: List[NestedZhviRecord] = []
            self.neighborhoods: List[NestedZhviRecord] = []

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

            zhvi_history = []

            history_start_index = pd_series.index.get_loc('2000-01-31')
            zhvi_history_df = pd_series.iloc[history_start_index:]
            for date, zhvi_value in zhvi_history_df.iterrows():
                if zhvi_value.iloc[0] is not None and zhvi_value.iloc[0] != "":
                    zhvi_history.append(
                        ZhviHistoryItem(
                            date=datetime.strptime(date, '%Y-%m-%d'),
                            zhvi_value=float(zhvi_value.iloc[0])
                        )
                    )
            self.zhvi_history = zhvi_history

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
            self.zhvi_history: List[ZhviHistoryItem] = zhvi_history
            self.metros: List[NestedZhviRecord] = metros
            self.cities: List[NestedZhviRecord] = cities
            self.neighborhoods: List[NestedZhviRecord] = neighborhoods

