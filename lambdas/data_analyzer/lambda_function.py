import logging

from components.event_manager.event_manager import EVENT_QUEUE_MODE_SNS
from data_analyzer.__main__ import Config
from components.event_manager.event_manager_sns import EventManagerSNS
from components.regions.region_data_gateway_mongo import RegionDataGatewayMongo
from data_analyzer.data_analyzer import DataAnalyzer


def lambda_handler(event, context):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)
    c = Config(event_queue_mode=EVENT_QUEUE_MODE_SNS)

    region_data_gateway = RegionDataGatewayMongo(db_uri=c.mongo_config.db_uri, db_name=c.mongo_config.db_name)
    event_manger = EventManagerSNS(
        region_name=c.event_sns_region,
        topic_arn=c.event_sns_topic_arn
    )
    data_analyzer = DataAnalyzer(event_manager=event_manger, region_data_gateway=region_data_gateway)

    sns_message = event['Records'][0]['Sns']['Message']
    data_analyzer.analyze_data(body=sns_message)


