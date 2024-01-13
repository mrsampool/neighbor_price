from typing import List
from datetime import datetime

from components.regions.region_data_gateway import RegionDataGateway
from components.regions.region_record import RegionRecord, RegionHistoryItem, RegionHistory


class RegionDataGatewayMock(RegionDataGateway):

    def __init__(self):
        super().__init__()

    def get_us_record(self) -> RegionRecord:
        return RegionRecord(
            region_id="0",
            region_name="United States of America",
            region_history=RegionHistory(
                items=[
                    RegionHistoryItem(
                        date=datetime(2023, 1, 1),
                        region_value=130
                    ),
                    RegionHistoryItem(
                        date=datetime(2023, 2, 1),
                        region_value=140
                    )
                ]
            )
        )

    def get_all_states(self) -> List[RegionRecord]:
        return [
            RegionRecord(
                region_id="state-1-id",
                region_name="state-1-name"
            ),
            RegionRecord(
                region_id="state-2-id",
                region_name="state-2-name"
            )
        ]

    def get_region_by_id(self, region_id):
        match region_id:
            case "1":
                return RegionRecord(
                    region_name="Colorado",
                    region_history=RegionHistory(
                        items=[
                            RegionHistoryItem(
                                date=datetime(2023, 1, 1),
                                region_value=150
                            ),
                            RegionHistoryItem(
                                date=datetime(2023, 2, 1),
                                region_value=160
                            )
                        ]
                    )
                )
            case "2":
                return RegionRecord(
                    region_name="metro-1",
                    state_name="CO",
                    region_history=RegionHistory(
                        items=[
                            RegionHistoryItem(
                                date=datetime(2023, 1, 1),
                                region_value=170
                            ),
                            RegionHistoryItem(
                                date=datetime(2023, 2, 1),
                                region_value=180
                            )
                        ]
                    )
                )
            case "4":
                return RegionRecord(
                    region_name="city-1",
                    state_name="CO",
                    region_history=RegionHistory(
                        items=[
                            RegionHistoryItem(
                                date=datetime(2023, 1, 1),
                                region_value=190
                            ),
                            RegionHistoryItem(
                                date=datetime(2023, 2, 1),
                                region_value=200
                            )
                        ]
                    )
                )
            case "7":
                return RegionRecord(
                    region_name="neighborhood-1",
                    state_name="CO",
                    region_history=RegionHistory(
                        items=[
                            RegionHistoryItem(
                                date=datetime(2023, 1, 1),
                                region_value=210
                            ),
                            RegionHistoryItem(
                                date=datetime(2023, 2, 1),
                                region_value=220
                            )
                        ]
                    )
                )

    def get_all_metros_for_state(self, state_name) -> List[RegionRecord]:
        match state_name:
            case "Colorado":
                return [
                    RegionRecord(
                        region_id="2",
                        region_name="metro-1"
                    ),
                    RegionRecord(
                        region_id="3",
                        region_name="metro-2"
                    )
                ]

    def get_all_cities_for_metro(self, metro_name, state_abbrev) -> List[RegionRecord]:
        if metro_name == "metro-1" and state_abbrev == "CO":
            return [
                RegionRecord(
                    region_id="4",
                    region_name="city-1"
                ),
                RegionRecord(
                    region_id="5",
                    region_name="city-2"
                ),
            ]

    def get_all_neighborhoods_for_city(self, city_name, state_abbrev) -> List[RegionRecord]:
        if city_name == "city-1" and state_abbrev == "CO":
            return [
                RegionRecord(
                    region_id="6",
                    region_name="neighborhood-1"
                ),
                RegionRecord(
                    region_id="7",
                    region_name="neighborhood-2"
                ),
            ]
