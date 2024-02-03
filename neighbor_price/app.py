#!/usr/bin/env python3
import json
import logging
import os

from flask import Flask, render_template, Response
from prometheus_client import Summary, generate_latest, CONTENT_TYPE_LATEST, Counter

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from components.regions.region_data_gateway_mongo import RegionDataGatewayMongo
from neighbor_price.region_detailer import RegionDetailer

app = Flask(__name__)
auth = HTTPBasicAuth()

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
page_view_counter = Counter('page_views', 'Total page views')
us_detail_counter = Counter('us_detail_views', 'US detail views')
state_detail_counter = Counter('state_detail_views', 'State detail views')
metro_detail_counter = Counter('metro_detail_views', 'Metro detail views')
city_detail_counter = Counter('city_detail_views', 'City detail views')
neighborhood_detail_counter = Counter('neighborhood_detail_views', 'Neighborhood Detail views')



@app.route("/")
@REQUEST_TIME.time()
def us_detail():
    page_view_counter.inc()
    us_detail_counter.inc()
    region_detail = region_detailer.get_us_detail()
    return render_template(
        template_name_or_list='neighborhood_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>")
@REQUEST_TIME.time()
def state_detail(state_id):
    page_view_counter.inc()
    state_detail_counter.inc()
    region_detail = region_detailer.get_state_detail(state_id=state_id)
    return render_template(
        template_name_or_list='state_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>")
@REQUEST_TIME.time()
def metro_detail(state_id, metro_id):
    page_view_counter.inc()
    metro_detail_counter.inc()
    region_detail = region_detailer.get_metro_detail(state_id=state_id, metro_id=metro_id)
    return render_template(
        template_name_or_list='metro_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>")
@REQUEST_TIME.time()
def city_detail(state_id, metro_id, city_id):
    page_view_counter.inc()
    city_detail_counter.inc()
    region_detail = region_detailer.get_city_detail(state_id=state_id, metro_id=metro_id, city_id=city_id)
    return render_template(
        template_name_or_list='city_detail.html',
        region_detail=region_detail
    )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>/neighborhood/<neighborhood_id>")
@REQUEST_TIME.time()
def neighborhood_detail(state_id, metro_id, city_id, neighborhood_id):
    page_view_counter.inc()
    neighborhood_detail_counter.inc()
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


users = {
    "grafana": generate_password_hash("grafanaadmin"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route('/metrics')
@auth.login_required
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/healthcheck")
@REQUEST_TIME.time()
def healthcheck():
    return json.dumps({'status': 'healthy'}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(port=8000, debug=True)