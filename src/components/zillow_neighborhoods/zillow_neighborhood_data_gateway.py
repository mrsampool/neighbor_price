#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy


class ZillowNeighborhoodDataGateway:
    def __init__(self, app):
        self.db = SQLAlchemy(app)

    def get_db(self):
        return self.db

    def get_session(self):
        return self.db.session

