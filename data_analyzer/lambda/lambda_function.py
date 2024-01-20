import logging

from data_analyzer.__main__ import Config
from components.event_manager.event_manager_sns import EventManagerSNS
from components.regions.region_data_gateway_mongo import RegionDataGatewayMongo
from data_analyzer.data_analyzer import DataAnalyzer


def lambda_handler(event, context):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)
    c = Config()

    region_data_gateway = RegionDataGatewayMongo(db_uri=c.regions_db_uri, db_name=c.regions_db_name)
    event_manger = EventManagerSNS()
    data_analyzer = DataAnalyzer(event_manager=event_manger, region_data_gateway=region_data_gateway)

    data_analyzer.analyze_data(body=event)
