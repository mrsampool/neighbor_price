from __future__ import annotations
from dataclasses import dataclass

from components.regions.region_data_gateway import RegionDataGateway
from neighbor_price.region_details import RegionDetail, RegionRecords, RegionPrices
from neighbor_price.region_links import StateLink, MetroLink, CityLink, NeighborhoodLink


@dataclass
class RegionDetailer:
    data_gateway: RegionDataGateway

    def get_us_detail(self) -> RegionDetail:
        us_record = self.data_gateway.get_us_record()
        state_records = self.data_gateway.get_all_states()
        return RegionDetail(
            region_records=RegionRecords(
                us=us_record
            ),
            links=list(map(lambda record: StateLink(
                region_id=record.region_id,
                label=record.region_name,
            ), state_records)),
            prices=RegionPrices(us=us_record.region_history.get_prices()),
            dates=us_record.region_history.get_dates()
        )

    def get_state_detail(self, state_id) -> RegionDetail:
        us_record = self.data_gateway.get_us_record()
        state_record = self.data_gateway.get_region_by_id(region_id=state_id)
        metro_records = self.data_gateway.get_all_metros_for_state(state_name=state_record.region_name)
        return RegionDetail(
            region_records=RegionRecords(
                us=us_record,
                state=state_record
            ),
            links=list(map(lambda record: MetroLink(
                label=record.region_name,
                region_id=record.region_id,
                state_id=state_id
            ), metro_records)),
            prices=RegionPrices(
                us=us_record.region_history.get_prices(),
                state=state_record.region_history.get_prices()
            ),
            dates=us_record.region_history.get_dates()
        )

    def get_metro_detail(self, state_id: str, metro_id: str) -> RegionDetail:
        us_record = self.data_gateway.get_us_record()
        state_record = self.data_gateway.get_region_by_id(region_id=state_id)
        metro_record = self.data_gateway.get_region_by_id(region_id=metro_id)
        city_records = self.data_gateway.get_all_cities_for_metro(
            metro_name=metro_record.region_name,
            state_abbrev=metro_record.state_name
        )
        return RegionDetail(
            region_records=RegionRecords(
                us=us_record,
                state=state_record,
                metro=metro_record,
            ),
            links=list(map(lambda record: CityLink(
                label=record.region_name,
                region_id=record.region_id,
                state_id=state_id,
                metro_id=metro_id
            ), city_records)),
            prices=RegionPrices(
                us=us_record.region_history.get_prices(),
                state=state_record.region_history.get_prices(),
                metro=metro_record.region_history.get_prices()
            ),
            dates=us_record.region_history.get_dates()
        )

    def get_city_detail(
            self,
            state_id: str,
            metro_id: str,
            city_id: str
    ) -> RegionDetail:
        us_record = self.data_gateway.get_us_record()
        state_record = self.data_gateway.get_region_by_id(region_id=state_id)
        metro_record = self.data_gateway.get_region_by_id(region_id=metro_id)
        city_record = self.data_gateway.get_region_by_id(region_id=city_id)
        neighborhood_records = self.data_gateway.get_all_neighborhoods_for_city(
            state_abbrev=metro_record.state_name,
            city_name=city_record.region_name
        )
        return RegionDetail(
            region_records=RegionRecords(
                us=us_record,
                state=state_record,
                metro=metro_record,
                city=city_record
            ),
            links=list(map(lambda record: NeighborhoodLink(
                label=record.region_name,
                region_id=record.region_id,
                state_id=state_id,
                metro_id=metro_id,
                city_id=city_id
            ), neighborhood_records)),
            prices=RegionPrices(
                us=us_record.region_history.get_prices(),
                state=state_record.region_history.get_prices(),
                metro=metro_record.region_history.get_prices(),
                city=city_record.region_history.get_prices()
            ),
            dates=us_record.region_history.get_dates()
        )

    def get_neighborhood_detail(
            self,
            state_id: str,
            metro_id: str,
            city_id: str,
            neighborhood_id: str
    ) -> RegionDetail:
        us_record = self.data_gateway.get_us_record()
        state_record = self.data_gateway.get_region_by_id(region_id=state_id)
        metro_record = self.data_gateway.get_region_by_id(region_id=metro_id)
        city_record = self.data_gateway.get_region_by_id(region_id=city_id)
        neighborhood_record = self.data_gateway.get_region_by_id(region_id=neighborhood_id)
        return RegionDetail(
            region_records=RegionRecords(
                us=us_record,
                state=state_record,
                metro=metro_record,
                city=city_record,
                neighborhood=neighborhood_record
            ),
            links=[],
            prices=RegionPrices(
                us=us_record.region_history.get_prices(),
                state=state_record.region_history.get_prices(),
                metro=metro_record.region_history.get_prices(),
                city=city_record.region_history.get_prices(),
                neighborhood=neighborhood_record.region_history.get_prices()
            ),
            dates=us_record.region_history.get_dates()
        )
