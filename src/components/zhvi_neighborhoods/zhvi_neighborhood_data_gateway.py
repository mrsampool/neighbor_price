#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import pymongo

from src.components.zhvi_neighborhoods.zhvi_neighborhood_record import ZhviNeighborhoodRecord, db

DB_COLLECTION_NEIGHBORHOODS = "neighborhoods"

class Base(DeclarativeBase):
    pass


class ZhviNeighborhoodDataGateway():
    def __init__(self, db_uri: str, db_name: str):
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[DB_COLLECTION_NEIGHBORHOODS]

    def create_neighborhood_record(
            self,
            record: ZhviNeighborhoodRecord = None,
            region_id: int = 0,
            size_rank: int = 0,
            region_name: str = "",
            region_type: str = "",
            state_name: str = "",
            state: str = "",
            city: str = "",
            metro: str = "",
            county_name: str = ""
    ):
        if record is None:
            record = ZhviNeighborhoodRecord(
                region_id=region_id,
                size_rank=size_rank,
                region_name=region_name,
                region_type=region_type,
                state_name=state_name,
                state=state,
                city=city,
                metro=metro,
                county_name=county_name,
            )
        self.collection.insert_one(record.to_doc())
