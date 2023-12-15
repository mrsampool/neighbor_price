#!/usr/bin/env python3

from flask import Flask, request, render_template
import logging
import os

from components.zhvi.zhvi_data_gateway import ZhviDataGateway

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
def states_list():
    states = zhvi_data_gateway.get_regions_by_type(region_type="state")
    page = "<ol>"
    page += "</ol>"
    return page


@app.route("/state/<state>/metros")
def state_metros_list(state):
    metros = zhvi_data_gateway.get_regions_by_type(region_type="msa")
    page = "<ol>"
    for metro in metros:
        page += f"<li><a href='/state/{metro['state_name']}/metros'>{state}</a></li>"
    page += "</ol>"
    return page


@app.route("/state/<state>/metro/<metro>/neighborhoods")
def metro_neighborhoods_list(state, metro):
    return f"{state} {metro}"


@app.route("/neighborhood/<neighborhood_id>")
def neighborhood(neighborhood_id):
    neighborhood_doc = zhvi_data_gateway.get_region_by_id(region_id=neighborhood_id)

    labels = [
        history.date
        for history in neighborhood_doc.zhvi_history
        if isinstance(history.zhvi_value, (int, float))
    ]
    data = [
        history.zhvi_value
        for history in neighborhood_doc.zhvi_history
        if isinstance(history.zhvi_value, (int, float))
    ]

    return render_template(
        template_name_or_list='neighborhood_detail.html',
        data=data,
        labels=labels,
    )


@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text
