#!/usr/bin/env python3

from flask import Flask, render_template
import logging
import os
from prometheus_client import start_http_server, Summary

from components.regions.region_data_gateway import RegionDataGateway
from neighbor_price.region_detailer import RegionDetail

db_uri = os.getenv("REGION_DB_URI")
logging.info(f"using REGION_DB_URI: {db_uri}")
if db_uri is None:
    logging.fatal("Missing required ENV: $REGION_DB_URI")

db_name = os.getenv("REGION_DB_NAME")
logging.info(f"using REGION_DB_NAME: {db_name}")
if db_name is None:
    logging.fatal("Missing required ENV: $REGION_DB_NAME")

region_data_gateway = RegionDataGateway(db_uri=db_uri, db_name=db_name)

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


@app.route("/")
@REQUEST_TIME.time()
def us_detail():
    region_detail = RegionDetail(
        region_data_gateway=region_data_gateway,
    )
    return render_template(
        template_name_or_list='neighborhood_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>")
@REQUEST_TIME.time()
def state_detail(state_id):
    region_detail = RegionDetail(
        region_data_gateway=region_data_gateway,
        state_id=state_id,
    )
    return render_template(
        template_name_or_list='state_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>")
@REQUEST_TIME.time()
def metro_detail(state_id, metro_id):
    region_detail = RegionDetail(
        region_data_gateway=region_data_gateway,
        state_id=state_id,
        metro_id=metro_id,
    )
    return render_template(
        template_name_or_list='metro_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>")
@REQUEST_TIME.time()
def city_detail(state_id, metro_id, city_id):
    region_detail = RegionDetail(
        region_data_gateway=region_data_gateway,
        state_id=state_id,
        metro_id=metro_id,
        city_id=city_id
    )
    return render_template(
        template_name_or_list='neighborhood_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>/neighborhood/<neighborhood_id>")
@REQUEST_TIME.time()
def neighborhood_detail(state_id, metro_id, city_id, neighborhood_id):
    region_detail = RegionDetail(
        region_data_gateway=region_data_gateway,
        state_id=state_id,
        metro_id=metro_id,
        city_id=city_id,
        neighborhood_id=neighborhood_id
    )
    return render_template(
        template_name_or_list='neighborhood_detail.html',
        region_detail=region_detail
    )


if __name__ == "__main__":
    start_http_server(8100)
    app.run(port=8000, debug=False)



