from datetime import datetime
class ZhviHistoryItem:
    def __init__(self, date: datetime, zhvi_value: float):
        self.date: datetime = date
        self.zhvi_value: float = zhvi_value
