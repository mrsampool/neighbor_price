#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from src.components.zillow_neighborhoods.zhvi_neighborhood_record import ZhviNeighborhoodRecord, db


class Base(DeclarativeBase):
    pass


class ZhviNeighborhoodDataGateway:
    def __init__(self, app, db_uri):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

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
        with self.app.app_context():
            db.session.add(record)
            db.session.commit()
