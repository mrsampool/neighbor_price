import json


class EventBody:
    def __init__(self, name, data):
        self.name = name,
        self.data = data

    def to_json(self):
        return json.dumps({
            "name": self.name,
            "data": self.data
        })
