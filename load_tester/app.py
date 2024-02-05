import random

import requests

base = "https://neighbor-cost-40ecba8d40ac.herokuapp.com"

paths = [
    "/state/9",
    "/",
    "/state/13",
    "/state/13/metro/394539",
    "/state/13/metro/394539/city/25711",
    "/",
    "/state/51",
    "/state/51/metro/394597",
    "/state/51/metro/394597/city/9687",
    "/",
    "/state/11",
    "/state/11/metro/395162",
    "/state/11/metro/395162/city/33133",
    "/",
    "/state/43",
    "/state/43/metro/394913",
    "/state/43/metro/394913/city/33074",
    "/state/43/metro/394913/city/33074/neighborhood/45396",
    "/",
    "/state/59",
    "/state/59/metro/395113",
    "/state/59/metro/395113/city/41000",
    "/",
    "/state/25",
    "/state/25/metro/394522"
    "/state/25/metro/394522/city/19330"
]

while True:
    path = random.choice(paths)
    url = base + path
    res = requests.get(url)
    print(res.status_code, res.url)