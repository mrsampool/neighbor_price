import logging

from components.event_manager.event_manager import EVENT_QUEUE_MODE_SNS
from components.region_csv_endpoint_worker.region_csv_endpoint_worker import RegionCsvEndpointWorker
from components.event_manager.event_manager_sns import EventManagerSNS
from data_collector.__main__ import Config
from data_collector.data_collector import DataCollector


def lambda_handler(event, context):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

    c = Config(event_queue_mode=EVENT_QUEUE_MODE_SNS)

    csv_client = RegionCsvEndpointWorker(
        region_csv_url=c.region_csv_url,
        neighborhood_csv_path=c.neighborhood_csv_path,
        city_csv_path=c.city_csv_path,
        metro_csv_path=c.metro_csv_path,
        state_csv_path=c.state_csv_path,
    )

    event_manager = EventManagerSNS(
        region_name=c.event_sns_region,
        topic_arn=c.event_sns_topic_arn
    )

    data_collector = DataCollector(
        csv_client=csv_client,
        event_manager=event_manager
    )

    data_collector.collect_all_data()
