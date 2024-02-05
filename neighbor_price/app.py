#!/usr/bin/env python3
import json
import logging
import os

from flask import Flask, render_template, Response
from prometheus_client import Summary, generate_latest, CONTENT_TYPE_LATEST, Counter, Gauge, Histogram

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

metrics_user = os.getenv("METRICS_USER")
logging.info(f"using METRICS_USER: {metrics_user}")
if metrics_user is None:
    logging.fatal("Missing required ENV: $METRICS_USER")

metrics_pw = generate_password_hash(os.getenv("METRICS_PW"))
if metrics_pw is None:
    logging.fatal("Missing required ENV: $METRICS_PW")


region_data_gateway = RegionDataGatewayMongo(db_uri=db_uri, db_name=db_name)
region_detailer = RegionDetailer(data_gateway=region_data_gateway)

REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP Request latency', ['method', 'page_type'])
PAGE_VIEWS = Counter('page_views_total', 'Total number of page views', ['page_type'])


@app.route("/")
def us_detail():
    page_type = "us detail"
    with REQUEST_LATENCY.labels(method='GET', page_type=page_type).time():
        PAGE_VIEWS.labels(page_type=page_type).inc()
        region_detail = region_detailer.get_us_detail()
        return render_template(
            template_name_or_list='neighborhood_detail.html',
            region_detail=region_detail
        )


@app.route("/state/<state_id>")
def state_detail(state_id):
    page_type = "state detail"
    with REQUEST_LATENCY.labels(method='GET', page_type=page_type).time():
        PAGE_VIEWS.labels(page_type=page_type).inc()
        region_detail = region_detailer.get_state_detail(state_id=state_id)
        return render_template(
            template_name_or_list='state_detail.html',
            region_detail=region_detail
        )


@app.route("/state/<state_id>/metro/<metro_id>")
def metro_detail(state_id, metro_id):
    page_type = "metro detail"
    with REQUEST_LATENCY.labels(method='GET', page_type=page_type).time():
        PAGE_VIEWS.labels(page_type=page_type).inc()
        region_detail = region_detailer.get_metro_detail(state_id=state_id, metro_id=metro_id)
        return render_template(
            template_name_or_list='metro_detail.html',
            region_detail=region_detail
        )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>")
def city_detail(state_id, metro_id, city_id):
    page_type = "city detail"
    with REQUEST_LATENCY.labels(method='GET', page_type=page_type).time():
        PAGE_VIEWS.labels(page_type=page_type).inc()
        region_detail = region_detailer.get_city_detail(state_id=state_id, metro_id=metro_id, city_id=city_id)
        return render_template(
            template_name_or_list='city_detail.html',
            region_detail=region_detail
        )


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>/neighborhood/<neighborhood_id>")
def neighborhood_detail(state_id, metro_id, city_id, neighborhood_id):
    page_type = "neighborhood detail"
    with REQUEST_LATENCY.labels(method='GET', page_type=page_type).time():
        PAGE_VIEWS.labels(page_type=page_type).inc()
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


@auth.verify_password
def verify_password(username, password):
    return username == metrics_user and check_password_hash(metrics_pw, password)


@app.route('/metrics')
@auth.login_required
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/healthcheck")
def healthcheck():
    return json.dumps({'status': 'healthy'}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(port=8000, debug=True)