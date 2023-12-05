#!/usr/bin/env python3
import requests
from flask import Flask
from io import StringIO
import pandas as pd

from components.zillow_neighborhoods.zillow_neighborhood_data_gateway import ZillowNeighborhoodDataGateway

app = Flask(__name__)

zn_gateway = ZillowNeighborhoodDataGateway(app)


def get_neighborhoods_df():
    response = requests.get(
        'https://files.zillowstatic.com/research/public_csvs/zhvi/Neighborhood_zhvi_bdrmcnt_3_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1701698974'
    )
    content = response.content.decode('utf-8')
    content_df = pd.read_csv(StringIO(content))
    return content_df


def create_neighborhoods_from_df(n_df):
    for i, neighborhood in n_df.iterrows():
        zn_gateway.create_neighborhood_record(
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


if __name__ == "__main__":
    neighborhoods_df = get_neighborhoods_df()
    create_neighborhoods_from_df(neighborhoods_df)


