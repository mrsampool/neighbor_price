import requests
import pandas as pd
from io import StringIO


class ZhviCsvClient:
    def __init__(
            self,
            zhvi_csv_url: str,
            zvhi_neighborhood_csv_path: str,
            zvhi_city_csv_path: str,
            zvhi_metro_csv_path: str,
            zvhi_state_csv_path: str
    ):
        self.zhvi_csv_url = zhvi_csv_url
        self.zhvi_neighborhood_csv_path = zvhi_neighborhood_csv_path
        self.zhvi_city_csv_path = zvhi_city_csv_path
        self.zhvi_metro_csv_path = zvhi_metro_csv_path
        self.zhvi_state_csv_path = zvhi_state_csv_path

    def _get_zhvi_df_from_path(self, path):
        response = requests.get(self.zhvi_csv_url + path)
        content = response.content.decode('utf-8')
        content_df = pd.read_csv(StringIO(content))
        return content_df

    def get_zhvi_neighborhoods_df(self):
        return self._get_zhvi_df_from_path(self.zhvi_neighborhood_csv_path)

    def get_zhvi_cities_df(self):
        return self._get_zhvi_df_from_path(self.zhvi_city_csv_path)

    def get_zhvi_metros_df(self):
        return self._get_zhvi_df_from_path(self.zhvi_metro_csv_path)

    def get_zhvi_states_df(self):
        return self._get_zhvi_df_from_path(self.zhvi_state_csv_path)
