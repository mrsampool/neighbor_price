import logging
import json
import pandas as pd
from io import StringIO

from components.event_manager.event_manager import EventManager
from components.regions.region_record import RegionRecord
from components.regions.region_data_gateway import RegionDataGateway


class DataAnalyzer:
    def __init__(
            self,
            event_manager: EventManager,
            region_data_gateway: RegionDataGateway
    ):
        self.event_manager = event_manager
        self.region_data_gateway = region_data_gateway

    def analyze_data(self, ch=None, method=None, properties=None, body=None):
        logging.info(f"analyzing_data: {body}")
        df = pd.read_csv(StringIO(body), index_col=0)

        record = RegionRecord(pd_series=df)
        logging.info(f"updating database: {record.region_type} {record.region_name}")
        self.region_data_gateway.save_region_record(record=record)
        if ch is not None:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def process_data(self, ch=None, method=None, properties=None, body=None):
        body = json.loads(body)
        data = body["data"]
        self.analyze_data(ch=ch, method=method, properties=properties, body=data)

    def analyze(self):
        self.event_manager.consume(callback=self.process_data)
