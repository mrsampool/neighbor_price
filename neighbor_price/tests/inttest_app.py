from neighbor_price.tests import collection
from neighbor_price.tests import client


def test_us_detail(client, collection):

    landing = client.get("/")
    html = landing.data.decode()

    # Check that links to `about` and `login` pages exist
    assert "<a href=\"/about/\">About</a>" in html
    assert " <a href=\"/home/\">Login</a>" in html

    # Spot check important text
    assert "At CultureMesh, we're building networks to match these " \
           "real-world dynamics and knit the diverse fabrics of our world " \
           "together." in html
    assert "1. Join a network you belong to." in html

    assert landing.status_code == 200
