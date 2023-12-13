import logging
from datetime import datetime

from components.zhvi_csv_client.zhvi_csv_client import ZhviCsvClient
from components.zhvi.zhvi_data_gateway import ZhviDataGateway
from components.zhvi.zhvi_record import ZhviRecord
from components.zhvi.zhvi_history_item import ZhviHistoryItem


def create_zhvi_record_from_df_row(df_row):
    region_id = df_row['RegionID']
    zhvi_history = []
    zhvi_history_df = df_row.iloc[9:]
    for date, zhvi_value in zhvi_history_df.items():
        zhvi_history.append(ZhviHistoryItem(date=datetime.strptime(date, '%Y-%m-%d'), zhvi_value=zhvi_value))

    return ZhviRecord(
        region_id=region_id,
        size_rank=df_row.get('SizeRank'),
        region_name=df_row.get('RegionName'),
        region_type=df_row.get('RegionType'),
        state_name=df_row.get('StateName'),
        state=df_row.get('State'),
        city=df_row.get('City'),
        metro=df_row.get('Metro'),
        county_name=df_row.get('CountyName'),
        zhvi_history=zhvi_history
    )


class DataCollector:
    def __init__(
            self,
            csv_client: ZhviCsvClient,
            zhvi_data_gateway: ZhviDataGateway
    ):
        self.csv_client = csv_client
        self.zhvi_data_gateway = zhvi_data_gateway

    def _fetch_zhvi_df_by_data_type(self, data_type: str):
        match data_type:
            case "neighborhoods":
                return self.csv_client.get_zhvi_neighborhoods_df()
            case "metros":
                return self.csv_client.get_zhvi_metros_df()
            case "states":
                return self.csv_client.get_zhvi_states_df()
            case _:
                logging.error(f"invalid ZHVI data type: {data_type}")
                return

    def _collect_zhvi_data(self, data_type: str):

        logging.info(f"collecting ZHVI {data_type} data")

        df = self._fetch_zhvi_df_by_data_type(data_type=data_type)
        total_rows = len(df.index)
        logging.info(f"collected ZHVI data for {total_rows} {data_type}. saving to database...")

        for i, df_row in df.iterrows():
            zhvi_record = create_zhvi_record_from_df_row(df_row)
            self.zhvi_data_gateway.create_zhvi_record(record=zhvi_record)
            if i % 100 == 0:
                logging.info(f"saving {data_type}... {total_rows - i} remaining...")

    def collect_neighborhoods_data(self):
        self._collect_zhvi_data(data_type="neighborhoods")

    def collect_metros_data(self):
        self._collect_zhvi_data(data_type="metros")

    def collect_states_data(self):
        self._collect_zhvi_data(data_type="states")
