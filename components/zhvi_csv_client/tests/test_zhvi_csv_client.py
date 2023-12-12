import unittest
import pandas as pd
from datetime import date
from components.zhvi_csv_client.zhvi_csv_client import create_zhvi_neighborhood_from_df_row


class TestZhviCsvClient(unittest.TestCase):

    def test_create_zhvi_neighborhood_from_df_row(self):
        neighborhood_df_row = pd.read_csv('./data/zhvi_neighborhoods.csv')

        actual = create_zhvi_neighborhood_from_df_row(df_row=neighborhood_df_row.loc[0])
        self.assertEqual(actual.region_id, 112345)
        self.assertEqual(actual.size_rank, 0)
        self.assertEqual(actual.region_name, "Maryvale")
        self.assertEqual(actual.region_type, "neighborhood")
        self.assertEqual(actual.state_name, "AZ")
        self.assertEqual(actual.state, "AZ")
        self.assertEqual(actual.city, "Phoenix")
        self.assertEqual(actual.metro, "Phoenix-Mesa-Chandler, AZ")
        self.assertEqual(actual.county_name, "Maricopa County")

        actual_history = actual.zhvi_history
        actual_history_1 = actual_history[0]
        self.assertEqual(date.isoformat(actual_history_1.date), "2000-01-31")
        self.assertEqual(actual_history_1.zhvi_value, 75553.2814897809)

    def test_create_zhvi_metro_from_df_row(self):
        metro_df_row = pd.read_csv('./data/zhvi_metros.csv')

        actual = create_zhvi_metro_from_df_row(df_row=metro_df_row.loc[0])
    def test_create_zhvi_state_from_df_row(self):
        state_df_row = pd.read_csv('./data/zhvi_states.csv')

        actual = create_zhvi_state_from_df_row(df_row=state_df_row.loc[0])