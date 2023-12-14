import logging

from components.zhvi_csv_client.zhvi_csv_client import ZhviCsvClient
from components.zhvi.zhvi_data_gateway import ZhviDataGateway

from components.event_manager.event_manager import EventManager
from components.event_manager.event_body import EventBody


class DataCollector:
    def __init__(
            self,
            csv_client: ZhviCsvClient,
            event_manager: EventManager,
            zhvi_data_gateway: ZhviDataGateway = None,
    ):
        self.csv_client = csv_client
        self.zhvi_data_gateway = zhvi_data_gateway
        self.event_manager = event_manager

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
        logging.info(f"collected raw ZHVI data for {total_rows} {data_type}. saving to database...")

        logging.info(f"publishing collected {data_type} ZHVI data...")
        for i, df_row in df.iterrows():
            row_csv = df_row.transpose().to_csv()
            self.event_manager.publish(body=EventBody(name="collected zhvi record", data=row_csv))

    def collect_neighborhoods_data(self):
        self._collect_zhvi_data(data_type="neighborhoods")

    def collect_metros_data(self):
        self._collect_zhvi_data(data_type="metros")

    def collect_states_data(self):
        self._collect_zhvi_data(data_type="states")
