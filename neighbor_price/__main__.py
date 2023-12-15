#!/usr/bin/env python3
import datetime

from flask import Flask, request, render_template
from typing import List
import logging
import os

from components.zhvi.zhvi_data_gateway import ZhviDataGateway
from components.zhvi.zhvi_history_item import ZhviHistoryItem

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


def prices_from_zhvi_history(history: List[ZhviHistoryItem]) -> List[float]:
    return [history.zhvi_value for history in history]


def dates_from_zhvi_history(history: List[ZhviHistoryItem]) -> List[datetime.datetime]:
    return [history.date for history in history]


@app.route("/state/<state_id>/metro/<metro_id>/city/<city_id>/neighborhood/<neighborhood_id>")
def neighborhood(state_id, metro_id, city_id, neighborhood_id):
    us_doc = zhvi_data_gateway.get_us_doc()
    state_doc = zhvi_data_gateway.get_region_by_id(region_id=state_id)
    metro_doc = zhvi_data_gateway.get_region_by_id(region_id=metro_id)
    city_doc = zhvi_data_gateway.get_region_by_id(region_id=city_id)
    neighborhood_doc = zhvi_data_gateway.get_region_by_id(region_id=neighborhood_id)

    dates = dates_from_zhvi_history(neighborhood_doc.zhvi_history)
    prices = {
        "neighborhood": prices_from_zhvi_history(neighborhood_doc.zhvi_history),
        "city": prices_from_zhvi_history(city_doc.zhvi_history),
        "metro": prices_from_zhvi_history(metro_doc.zhvi_history),
        "state": prices_from_zhvi_history(state_doc.zhvi_history),
        "us": prices_from_zhvi_history(us_doc.zhvi_history)
    }

    return render_template(
        template_name_or_list='neighborhood_detail.html',
        dates=dates,
        neighborhood=neighborhood_doc,
        neighborhood_prices=prices['neighborhood'],
        city_prices=prices['city'],
        metro_prices=prices['metro'],
        state_prices=prices['state'],
        us_prices=prices['us']
    )


@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text


if __name__ == "__main__":
    app.run(port=8000, debug=True)
