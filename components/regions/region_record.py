from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class RegionHistoryItem:
    date: datetime
    region_value: float


@dataclass
class RegionHistory:

    def __init__(
            self,
            items: List[RegionHistoryItem] = None,
            doc_history=None
    ):
        if items is not None:
            self.history_items = items

        else:
            self.history_items = []
            if doc_history is not None:
                for history_item in doc_history:
                    self.history_items.append(
                        RegionHistoryItem(
                            date=history_item["date"],
                            region_value=float(history_item["region_value"])
                        )
                    )

    def add_item(self, item: RegionHistoryItem):
        self.history_items.append(item)

    def get_prices(self) -> List[float]:
        return [history.region_value for history in self.history_items]

    def get_dates(self) -> List[str]:
        return [history.date.strftime("%Y-%m") for history in self.history_items]


def get_average_value_growth_rate(region_history: RegionHistory) -> float:
    prices = region_history.get_prices()
    if len(prices) < 1:
        return 0
    percentage_changes = [
        (prices[i + 1] - prices[i]) / prices[i] * 100 for i in range(len(prices) - 1)
    ]
    average_rate_of_growth = sum(percentage_changes) / len(percentage_changes)
    return round(average_rate_of_growth, 2)


class RegionRecord:
    def __init__(
            self,
            document=None,
            pd_series=None,
            region_id: str = None,
            size_rank: int = None,
            region_name: str = None,
            region_type: str = None,
            state_name: str = None,
            state: str = None,
            city: str = None,
            metro: str = None,
            county_name: str = None,
            region_history: RegionHistory = None,
    ):
        self.average_value_growth_rate = None

        if document is not None:
            self.init_from_document(document=document)

        elif pd_series is not None:
            self.init_from_pd_series(pd_series=pd_series)

        else:
            self.region_id: str = region_id
            self.size_rank: int = size_rank
            self.region_name: str = region_name
            self.region_type: str = region_type
            self.state_name: str = state_name
            self.state: str = state
            self.city: str = city
            self.metro: str = metro
            self.county_name: str = county_name
            self.region_history: RegionHistory = region_history if region_history is not None else RegionHistory()

        if self.average_value_growth_rate is None:
            self.average_value_growth_rate = get_average_value_growth_rate(self.region_history)

    def init_from_document(self, document):
        self.region_id: int = document.get("region_id")
        self.size_rank: int = document.get("size_rank")
        self.region_name: str = document.get("region_name")
        self.region_type: str = document.get("region_type")
        self.state_name: str = document.get("state_name")
        self.state: str = document.get("state")
        self.city: str = document.get("city")
        self.metro: str = document.get("metro")
        self.county_name: str = document.get("county_name")
        self.region_history = []
        self.region_history = RegionHistory(doc_history=document.get("region_history"))
        doc_growth_rate = document.get("average_value_growth_rate")
        if doc_growth_rate == "":
            self.average_value_growth_rate = None
        else:
            self.average_value_growth_rate = doc_growth_rate

    def init_from_pd_series(self, pd_series):
        self.region_id: int = pd_series.loc['RegionID'].iloc[0]
        self.size_rank: int = pd_series.loc['SizeRank'].iloc[0]
        self.region_name: str = pd_series.loc['RegionName'].iloc[0]
        self.region_type: str = pd_series.loc['RegionType'].iloc[0]
        self.state_name: str = pd_series.loc['StateName'].iloc[0]

        cols = pd_series.index.values

        if 'State' in cols:
            self.state: str = pd_series.loc['State'].iloc[0]
        else:
            self.state = None

        if 'City' in cols:
            self.city: str = pd_series.loc['City'].iloc[0]
        else:
            self.city = None

        if 'Metro' in cols:
            self.metro = pd_series.loc['Metro'].iloc[0]
        else:
            self.metro = None

        if 'CountyName' in cols:
            self.county_name: str = pd_series.loc['CountyName'].iloc[0]
        else:
            self.county_name = None

        region_history = RegionHistory()

        history_start_index = pd_series.index.get_loc('2000-01-31')
        region_history_df = pd_series.iloc[history_start_index:]
        for date, region_value in region_history_df.iterrows():
            if region_value.iloc[0] is not None and region_value.iloc[0] != "":
                region_history.add_item(
                    RegionHistoryItem(
                        date=datetime.strptime(date, '%Y-%m-%d'),
                        region_value=float(region_value.iloc[0])
                    )
                )
        self.region_history = region_history
