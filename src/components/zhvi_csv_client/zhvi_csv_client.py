import requests
import pandas as pd
from io import StringIO

from src.components.zillow_neighborhoods.zillow_neighborhood_record import ZillowNeighborhoodRecord


class ZhviCsvClient:
    def __init__(
            self,
            zhvi_csv_url: str,
            zvhi_neighborhood_csv_path: str
    ):
        self.zhvi_csv_url = zhvi_csv_url
        self.zhvi_neighborhood_csv_path = zvhi_neighborhood_csv_path

    def get_zhvi_df_from_path(self, path):
        response = requests.get(self.zhvi_csv_url + path)
        content = response.content.decode('utf-8')
        content_df = pd.read_csv(StringIO(content))
        return content_df

    def get_zhvi_neighborhoods_df(self):
        self.get_zhvi_df_from_path(self.zhvi_neighborhood_csv_path)

    def create_zhvi_neighborhood_from_df_row(self, df_row):
        return ZillowNeighborhoodRecord(
            region_id=df_row['RegionID'],
            size_rank=df_row['SizeRank'],
            region_name=df_row['RegionName'],
            region_type=df_row['RegionType'],
            state_name=df_row['StateName'],
            state=df_row['State'],
            city=df_row['City'],
            metro=df_row['Metro'],
            county_name=df_row['CountyName'],
        )
