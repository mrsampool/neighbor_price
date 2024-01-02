import logging

from components.event_manager.event_manager import EventManager
import json
import pandas as pd
from io import StringIO

from components.zhvi.zhvi_record import ZhviRecord, NestedZhviRecord
from components.zhvi.zhvi_data_gateway import ZhviDataGateway


class DataAnalyzer:
    def __init__(
            self,
            event_manager: EventManager,
            zhvi_data_gateway: ZhviDataGateway
    ):
        self.event_manager = event_manager
        self.zhvi_data_gateway = zhvi_data_gateway

    def populate_nested_zhvi_record_fields(self, record: ZhviRecord) -> ZhviRecord:
        match record.region_type:
            case 'state':
                metro_records = self.zhvi_data_gateway.get_all_metros_for_state_from_name(record.region_name)
                record.metros = []
                for metro_record in metro_records:
                    record.metros.append(
                        NestedZhviRecord(
                            region_id=metro_record.region_id,
                            region_name=metro_record.region_name
                        )
                    )
            case 'msa':
                city_records = self.zhvi_data_gateway.get_all_cities_for_metro_from_name(record.region_name)
                record.cities = []
                for city_record in city_records:
                    record.cities.append(
                        NestedZhviRecord(
                            region_id=city_record.region_id,
                            region_name=city_record.region_name
                        )
                    )
            case 'city':
                neighborhood_records = self.zhvi_data_gateway.get_all_neighborhoods_for_city_from_name(record.region_name)
                record.neighborhoods = []
                for neighborhood_record in neighborhood_records:
                    record.neighborhoods.append(
                        NestedZhviRecord(
                            region_id=neighborhood_record.region_id,
                            region_name=neighborhood_record.region_name
                        )
                    )
        return record

    def analyze_data(self, ch=None, method=None, properties=None, body=None):
        body = json.loads(body)
        data = body["data"]
        df = pd.read_csv(StringIO(data), index_col=0)

        record = ZhviRecord(pd_series=df)
        record = self.populate_nested_zhvi_record_fields(record=record)
        logging.info(f"updating database: {record.region_type} {record.region_name}")
        self.zhvi_data_gateway.create_zhvi_record(record=record)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def analyze(self):
        self.event_manager.consume(callback=self.analyze_data)
