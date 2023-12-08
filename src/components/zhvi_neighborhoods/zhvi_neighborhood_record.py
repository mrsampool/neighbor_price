from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class ZhviNeighborhoodRecord:
    def __init__(
            self,
            document = None,
            region_id: int = None,
            size_rank: int = None,
            region_name: str = None,
            region_type: str = None,
            state_name: str = None,
            state: str = None,
            city: str = None,
            metro: str = None,
            county_name: str = None
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

    def to_doc(self):
        return {
            "region_id": self.region_id,
            "size_rank": self.size_rank,
            "region_name": self.region_name,
            "region_type": self.region_type,
            "state_name": self.state_name,
            "state": self.state,
            "city": self.city,
            "metro": self.metro,
            "county_name": self.county_name
        }
