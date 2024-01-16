import logging

from components.region_csv_endpoint_worker.region_csv_endpoint_worker import RegionCsvEndpointWorker

from components.event_manager.event_manager import EventManager
from components.event_manager.event_body import EventBody


class DataCollector:
    def __init__(
            self,
            csv_client: RegionCsvEndpointWorker,
            event_manager: EventManager,
    ):
        self.csv_client = csv_client
        self.event_manager = event_manager

    def _fetch_region_df_by_region_type(self, data_type: str):
        match data_type:
            case "neighborhoods":
                return self.csv_client.get_neighborhoods_df()
            case "cities":
                return self.csv_client.get_cities_df()
            case "metros":
                return self.csv_client.get_metros_df()
            case "states":
                return self.csv_client.get_states_df()
            case _:
                logging.error(f"invalid region data type: {data_type}")
                return

    def _collect_region_data(self, data_type: str):

        logging.info(f"collecting  {data_type} data")

        df = self._fetch_region_df_by_region_type(data_type=data_type)
        total_rows = len(df.index)
        logging.info(f"collected raw  data for {total_rows} {data_type}. saving to database...")

        logging.info(f"publishing collected {data_type}  data...")
        for i, df_row in df.iterrows():
            row_csv = df_row.to_csv()
            self.event_manager.publish(body=EventBody(name="collected region record", data=row_csv))

    def collect_neighborhoods_data(self):
        self._collect_region_data(data_type="neighborhoods")

    def collect_cities_data(self):
        self._collect_region_data(data_type="cities")

    def collect_metros_data(self):
        self._collect_region_data(data_type="metros")

    def collect_states_data(self):
        self._collect_region_data(data_type="states")
