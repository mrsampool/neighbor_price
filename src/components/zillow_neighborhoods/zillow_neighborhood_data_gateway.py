#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from src.components.zillow_neighborhoods.zillow_neighborhood_record import ZillowNeighborhoodRecord, db


class Base(DeclarativeBase):
    pass


class ZillowNeighborhoodDataGateway:
    def __init__(self, app):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NeighborCost.sqlite3'
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def create_neighborhood_record(
            self,
            region_id: int,
            size_rank: int,
            region_name: str,
            region_type: str,
            state_name: str,
            state: str,
            city: str,
            metro: str,
            county_name: str
    ):
        n = ZillowNeighborhoodRecord(
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
            db.session.add(n)
            db.session.commit()
