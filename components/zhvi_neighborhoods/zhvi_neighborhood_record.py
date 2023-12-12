from typing import List
from flask_sqlalchemy import SQLAlchemy

from components.zhvi_history.zhvi_history_item import ZhviHistoryItem

db = SQLAlchemy()


class ZhviNeighborhoodRecord:
    def __init__(
            self,
            document=None,
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
