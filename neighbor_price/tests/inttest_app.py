from neighbor_price.tests import collection
from neighbor_price.tests import client


def test_us_detail(client, collection):
    landing = client.get("/")
    assert landing.status_code == 200

    html = landing.data.decode()

    assert '<a href="/state/9">' in html
    assert "California" in html

    assert '<a href="/state/54">' in html
    assert "Texas" in html

    assert '<canvas id="region-chart"' in html


def test_state_detail(client, collection):
    landing = client.get("/state/9")
    assert landing.status_code == 200

    html = landing.data.decode()

    assert '<h1>California</h1>' in html

    assert '<a href="/state/9/metro/395057">' in html
    assert "San Francisco" in html

    assert '<a href="/state/9/metro/753899">' in html
    assert "Los Angeles" in html

    assert '<canvas id="region-chart"' in html


def test_metro_detail(client, collection):
    landing = client.get("/state/9/metro/395057")
    assert landing.status_code == 200

    html = landing.data.decode()

    assert '<h1>San Francisco, CA</h1>' in html

    assert '<a href="/state/9/metro/395057/city/20330">' in html
    assert "San Francisco" in html

    assert '<a href="/state/9/metro/395057/city/13072">' in html
    assert "Oakland" in html

    assert '<canvas id="region-chart"' in html


def test_city_detail(client, collection):
    landing = client.get("/state/9/metro/395057/city/20330")
    assert landing.status_code == 200

    html = landing.data.decode()

    assert '<h1>San Francisco</h1>' in html

    assert '<a href="/state/9/metro/395057/city/20330/neighborhood/268450">' in html
    assert "Russian Hill" in html

    assert '<a href="/state/9/metro/395057/city/20330/neighborhood/268337">' in html
    assert "Nob Hill" in html

    assert '<canvas id="region-chart"' in html

def test_neighborhood_detail(client, collection):
    landing = client.get("/state/9/metro/395057/city/20330/neighborhood/268450")
    assert landing.status_code == 200

    html = landing.data.decode()

    assert '<h1>Russian Hill</h1>' in html

    assert '<canvas id="region-chart"' in html
