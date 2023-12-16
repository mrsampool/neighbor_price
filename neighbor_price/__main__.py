#!/usr/bin/env python3
from flask import Flask, render_template
import logging
import os

from components.zhvi.zhvi_data_gateway import ZhviDataGateway
from neighbor_price.region_detail import RegionDetail

db_uri = os.getenv("ZHVI_DB_URI")
logging.info(f"using ZHVI_DB_URI: {db_uri}")
if db_uri is None:
    logging.fatal("Missing required ENV: $ZHVI_DB_URI")

db_name = os.getenv("ZHVI_DB_NAME")
logging.info(f"using ZHVI_DB_NAME: {db_name}")
if db_name is None:
    logging.fatal("Missing required ENV: $ZHVI_DB_NAME")

zhvi_data_gateway = ZhviDataGateway(db_uri=db_uri, db_name=db_name)

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=20)


@app.route("/")
def us_detail():
    region_detail = RegionDetail(
        zhvi_data_gateway=zhvi_data_gateway,
    )
    return render_template(
        template_name_or_list='neighborhood_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>")
def state_detail(state_id):
    region_detail = RegionDetail(
        zhvi_data_gateway=zhvi_data_gateway,
        state_id=state_id,
    )
    return render_template(
        template_name_or_list='state_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>")
def metro_detail(state_id, metro_id):
    region_detail = RegionDetail(
        zhvi_data_gateway=zhvi_data_gateway,
        state_id=state_id,
        metro_id=metro_id,
    )
    return render_template(
        template_name_or_list='metro_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>")
def city_detail(state_id, metro_id, city_id):
    region_detail = RegionDetail(
        zhvi_data_gateway=zhvi_data_gateway,
        state_id=state_id,
        metro_id=metro_id,
        city_id=city_id
    )
    return render_template(
        template_name_or_list='neighborhood_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>/neighborhood/<neighborhood_id>")
def neighborhood_detail(state_id, metro_id, city_id, neighborhood_id):
    region_detail = RegionDetail(
        zhvi_data_gateway=zhvi_data_gateway,
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
    app.run(port=8000, debug=True)
