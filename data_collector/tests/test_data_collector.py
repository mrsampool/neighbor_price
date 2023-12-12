import unittest
from data_collector.__main__ import handler


class TestDataCollector(unittest.TestCase):

    def test_handler(self):
        handler()
