import logging

from components.event_manager.event_manager import EventManager
import json
import pandas as pd
from io import StringIO

from components.zhvi.zhvi_record import ZhviRecord
from components.zhvi.zhvi_data_gateway import ZhviDataGateway


class DataAnalyzer:
    def __init__(
            self,
            event_manager: EventManager,
            zhvi_data_gateway: ZhviDataGateway
    ):
        self.event_manager = event_manager
        self.zhvi_data_gateway = zhvi_data_gateway

    def analyze_data(self, ch=None, method=None, properties=None, body=None):
        body = json.loads(body)
        data = body["data"]
        df = pd.read_csv(StringIO(data), index_col=0)

        record = ZhviRecord(pd_series=df)
        logging.info(f"updating database: {record.region_type} {record.region_name}")
        self.zhvi_data_gateway.create_zhvi_record(record=record)

    def analyze(self):
        self.event_manager.consume(callback=self.analyze_data)
