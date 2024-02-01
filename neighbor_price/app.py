#!/usr/bin/env python3
import json
import logging
import os

from flask import Flask, render_template
from prometheus_client import start_http_server, Summary

from components.regions.region_data_gateway_mongo import RegionDataGatewayMongo
from neighbor_price.region_detailer import RegionDetailer

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

db_uri = os.getenv("REGION_DB_URI")
logging.info(f"using REGION_DB_URI: {db_uri}")
if db_uri is None:
    logging.fatal("Missing required ENV: $REGION_DB_URI")

db_name = os.getenv("REGION_DB_NAME")
logging.info(f"using REGION_DB_NAME: {db_name}")
if db_name is None:
    logging.fatal("Missing required ENV: $REGION_DB_NAME")

region_data_gateway = RegionDataGatewayMongo(db_uri=db_uri, db_name=db_name)
region_detailer = RegionDetailer(data_gateway=region_data_gateway)

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


@app.route("/")
@REQUEST_TIME.time()
def us_detail():
    region_detail = region_detailer.get_us_detail()
    return render_template(
        template_name_or_list='neighborhood_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>")
@REQUEST_TIME.time()
def state_detail(state_id):
    region_detail = region_detailer.get_state_detail(state_id=state_id)
    return render_template(
        template_name_or_list='state_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>")
@REQUEST_TIME.time()
def metro_detail(state_id, metro_id):
    region_detail = region_detailer.get_metro_detail(state_id=state_id, metro_id=metro_id)
    return render_template(
        template_name_or_list='metro_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>")
@REQUEST_TIME.time()
def city_detail(state_id, metro_id, city_id):
    region_detail = region_detailer.get_city_detail(state_id=state_id, metro_id=metro_id, city_id=city_id)
    return render_template(
        template_name_or_list='city_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>/neighborhood/<neighborhood_id>")
@REQUEST_TIME.time()
def neighborhood_detail(state_id, metro_id, city_id, neighborhood_id):
    region_detail = region_detailer.get_neighborhood_detail(
        state_id=state_id,
        metro_id=metro_id,
        city_id=city_id,
        neighborhood_id=neighborhood_id
    )
    return render_template(
        template_name_or_list='neighborhood_detail.html',
        region_detail=region_detail
    )


@app.route("/healthcheck")
@REQUEST_TIME.time()
def healthcheck():
    return json.dumps({'status': 'healthy'}), 200, {'ContentType': 'application/json'}


start_http_server(8100)

if __name__ == "__main__":
    start_http_server(8100)
    app.run(port=8000, debug=True)
