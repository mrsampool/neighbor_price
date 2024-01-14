import requests
import pandas as pd
from io import StringIO


class RegionCsvEndpointWorker:
    def __init__(
            self,
            region_csv_url: str,
            neighborhood_csv_path: str,
            city_csv_path: str,
            metro_csv_path: str,
            state_csv_path: str
    ):
        self.region_csv_url = region_csv_url
        self.neighborhood_csv_path = neighborhood_csv_path
        self.city_csv_path = city_csv_path
        self.metro_csv_path = metro_csv_path
        self.state_csv_path = state_csv_path

    def _get_region_df_from_path(self, path):
        response = requests.get(self.region_csv_url + path)
        content = response.content.decode('utf-8')
        content_df = pd.read_csv(StringIO(content), keep_default_na=False)
        return content_df

    def get_neighborhoods_df(self):
        return self._get_region_df_from_path(self.neighborhood_csv_path)

    def get_cities_df(self):
        return self._get_region_df_from_path(self.city_csv_path)

    def get_metros_df(self):
        return self._get_region_df_from_path(self.metro_csv_path)

    def get_states_df(self):
        return self._get_region_df_from_path(self.state_csv_path)
