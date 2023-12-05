#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from io import StringIO
import pandas as pd


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NeighborCost.sqlite3'

db.init_app(app)


class ZillowNeighborhoodRecord(db.Model):
    region_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    size_rank: Mapped[int] = mapped_column(Integer, nullable=True)
    region_name: Mapped[str] = mapped_column(String, nullable=True)
    region_type: Mapped[str] = mapped_column(String, nullable=True)
    state_name: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)
    metro: Mapped[str] = mapped_column(String, nullable=True)
    county_name: Mapped[str] = mapped_column(String, nullable=True)


with app.app_context():
    db.create_all()


def get_neighborhoods_df():
    response = requests.get(
        'https://files.zillowstatic.com/research/public_csvs/zhvi/Neighborhood_zhvi_bdrmcnt_3_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1701698974'
    )
    content = response.content.decode('utf-8')
    content_df = pd.read_csv(StringIO(content))
    return content_df


def create_neighborhoods_from_df(neighborhoods_df):
    for i, neighborhood in neighborhoods_df.iterrows():
        n = ZillowNeighborhoodRecord(
            region_id=neighborhood['RegionID'],
            size_rank=neighborhood['SizeRank'],
            region_name=neighborhood['RegionName'],
            region_type=neighborhood['RegionType'],
            state_name=neighborhood['StateName'],
            state=neighborhood['State'],
            city=neighborhood['City'],
            metro=neighborhood['Metro'],
            county_name=neighborhood['CountyName'],
        )
        with app.app_context():
            db.session.add(n)
            db.session.commit()


if __name__ == "__main__":
    neighborhoods_df = get_neighborhoods_df()
    create_neighborhoods_from_df(neighborhoods_df)


