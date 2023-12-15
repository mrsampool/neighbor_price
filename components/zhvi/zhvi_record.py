import logging
from typing import List
from datetime import datetime

from components.zhvi.zhvi_history_item import ZhviHistoryItem


class ZhviRecord:
    def __init__(
            self,
            document=None,
            pd_series=None,
            region_id: int = None,
            size_rank: int = None,
            region_name: str = None,
            region_type: str = None,
            state_name: str = None,
            state: str = None,
            city: str = None,
            metro: str = None,
            county_name: str = None,
            zhvi_history: List[ZhviHistoryItem] = []
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
            self.zhvi_history: List[ZhviHistoryItem] = document["zhvi_history"]

        elif pd_series is not None:
            self.region_id: int = pd_series.loc['RegionID'].iloc[0]
            self.size_rank: int = pd_series.loc['SizeRank'].iloc[0]
            self.region_name: str = pd_series.loc['RegionName'].iloc[0]
            self.region_type: str = pd_series.loc['RegionType'].iloc[0]
            self.state_name: str = pd_series.loc['StateName'].iloc[0]

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
                self.metro: str = pd_series.loc['Metro'].iloc[0]
            else:
                self.metro = None

            if 'CountyName' in cols:
                self.county_name: str = pd_series.loc['CountyName'].iloc[0]
            else:
                self.county_name = None

            zhvi_history = []
            zhvi_history_df = pd_series.iloc[9:]
            for date, zhvi_value in zhvi_history_df.iterrows():
                zhvi_history.append(ZhviHistoryItem(date=datetime.strptime(date, '%Y-%m-%d'), zhvi_value=zhvi_value.iloc[0]))
            self.zhvi_history = zhvi_history

        else:
            self.region_id: int = region_id
            self.size_rank: int = size_rank
            self.region_name: str = region_name
            self.region_type: str = region_type
            self.state_name: str = state_name
            self.state: str = state
            self.city: str = city
            self.metro: str = metro
            self.county_name: str = county_name
            self.zhvi_history: List[ZhviHistoryItem] = zhvi_history
