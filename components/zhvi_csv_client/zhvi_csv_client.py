import requests
import pandas as pd
from io import StringIO
from datetime import datetime

from components.zhvi_neighborhoods.zhvi_neighborhood_record import ZhviNeighborhoodRecord
from components.zhvi_history.zhvi_history_item import ZhviHistoryItem


def create_zhvi_neighborhood_from_df_row(df_row):
    region_id = df_row['RegionID']
    zhvi_history = []
    zhvi_history_df = df_row.iloc[9:]
    for date, zhvi_value in zhvi_history_df.items():
        zhvi_history.append(ZhviHistoryItem(date=datetime.strptime(date, '%Y-%m-%d'), zhvi_value=zhvi_value))

    return ZhviNeighborhoodRecord(
        region_id=region_id,
        size_rank=df_row['SizeRank'],
        region_name=df_row['RegionName'],
        region_type=df_row['RegionType'],
        state_name=df_row['StateName'],
        state=df_row['State'],
        city=df_row['City'],
        metro=df_row['Metro'],
        county_name=df_row['CountyName'],
        zhvi_history=zhvi_history
    )


class ZhviCsvClient:
    def __init__(
            self,
            zhvi_csv_url: str,
            zvhi_neighborhood_csv_path: str,
            zvhi_metro_csv_path: str,
            zvhi_state_csv_path: str
    ):
        self.zhvi_csv_url = zhvi_csv_url
        self.zhvi_neighborhood_csv_path = zvhi_neighborhood_csv_path
        self.zhvi_metro_csv_path = zvhi_metro_csv_path
        self.zhvi_state_csv_path = zvhi_state_csv_path

    def _get_zhvi_df_from_path(self, path):
        response = requests.get(self.zhvi_csv_url + path)
        content = response.content.decode('utf-8')
        content_df = pd.read_csv(StringIO(content))
        return content_df

    def get_zhvi_neighborhoods_df(self):
        return self._get_zhvi_df_from_path(self.zhvi_neighborhood_csv_path)

    def get_zhvi_metros_df(self):
        return self._get_zhvi_df_from_path(self.zhvi_metro_csv_path)

    def get_zhvi_states_df(self):
        return self._get_zhvi_df_from_path(self.zhvi_state_csv_path)
