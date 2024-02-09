from __future__ import annotations
from dataclasses import dataclass

from components.regions.region_data_gateway import RegionDataGateway
from neighbor_price.region_details import RegionDetail, RegionRecords, RegionPrices
from neighbor_price.region_links import StateLink, MetroLink, CityLink, NeighborhoodLink


@dataclass
class RegionDetailer:
    data_gateway: RegionDataGateway

    def get_region_records(
            self,
            state_id: str | None = None,
            metro_id: str | None = None,
            city_id: str | None = None,
            neighborhood_id: str | None = None
    ) -> RegionRecords:

        u_r = self.data_gateway.get_us_record()
        s_r = self.data_gateway.get_region_by_id(region_id=state_id) if state_id is not None else None
        m_r = self.data_gateway.get_region_by_id(region_id=metro_id) if metro_id is not None else None
        c_r = self.data_gateway.get_region_by_id(region_id=city_id) if city_id is not None else None
        n_r = self.data_gateway.get_region_by_id(region_id=neighborhood_id) if neighborhood_id is not None else None

        return RegionRecords(
            us=u_r,
            state=s_r,
            metro=m_r,
            city=c_r,
            neighborhood=n_r
        )

    def get_us_detail(self) -> RegionDetail:
        region_records = self.get_region_records()
        state_records = self.data_gateway.get_all_states()
        return RegionDetail(
            region_records=region_records,
            links=list(map(lambda record: StateLink(
                region_id=record.region_id,
                label=record.region_name,
            ), state_records)),
            prices=region_records.get_prices(),
            dates=region_records.us.region_history.get_dates(),
            growth_rate=region_records.us.average_value_growth_rate,
            breadcrumbs=region_records.get_breadcrumbs()
        )

    def get_state_detail(self, state_id) -> RegionDetail:
        region_records = self.get_region_records(state_id=state_id)
        metro_records = self.data_gateway.get_all_metros_for_state(state_name=region_records.state.region_name)
        return RegionDetail(
            region_records=region_records,
            links=list(map(lambda record: MetroLink(
                label=record.region_name,
                region_id=record.region_id,
                state_id=state_id
            ), metro_records)),
            prices=region_records.get_prices(),
            dates=region_records.us.region_history.get_dates(),
            growth_rate=region_records.state.average_value_growth_rate,
            breadcrumbs=region_records.get_breadcrumbs()
        )

    def get_metro_detail(self, state_id: str, metro_id: str) -> RegionDetail:
        region_records = self.get_region_records(state_id=state_id, metro_id=metro_id)
        city_records = self.data_gateway.get_all_cities_for_metro(
            metro_name=region_records.metro.region_name,
            state_abbrev=region_records.metro.state_name
        )
        return RegionDetail(
            region_records=region_records,
            links=list(map(lambda record: CityLink(
                label=record.region_name,
                region_id=record.region_id,
                state_id=state_id,
                metro_id=metro_id
            ), city_records)),
            prices=region_records.get_prices(),
            dates=region_records.us.region_history.get_dates(),
            growth_rate=region_records.metro.average_value_growth_rate,
            breadcrumbs=region_records.get_breadcrumbs()
        )

    def get_city_detail(
            self,
            state_id: str,
            metro_id: str,
            city_id: str
    ) -> RegionDetail:
        region_records = self.get_region_records(
            state_id=state_id,
            metro_id=metro_id,
            city_id=city_id
        )
        neighborhood_records = self.data_gateway.get_all_neighborhoods_for_city(
            state_abbrev=region_records.metro.state_name,
            city_name=region_records.city.region_name
        )
        return RegionDetail(
            region_records=region_records,
            links=list(map(lambda record: NeighborhoodLink(
                label=record.region_name,
                region_id=record.region_id,
                state_id=state_id,
                metro_id=metro_id,
                city_id=city_id
            ), neighborhood_records)),
            prices=region_records.get_prices(),
            dates=region_records.us.region_history.get_dates(),
            growth_rate=region_records.city.average_value_growth_rate,
            breadcrumbs=region_records.get_breadcrumbs()
        )

    def get_neighborhood_detail(
            self,
            state_id: str,
            metro_id: str,
            city_id: str,
            neighborhood_id: str
    ) -> RegionDetail:
        region_records = self.get_region_records(
            state_id=state_id,
            metro_id=metro_id,
            city_id=city_id,
            neighborhood_id=neighborhood_id
        )
        return RegionDetail(
            region_records=region_records,
            links=[],
            prices=region_records.get_prices(),
            dates=region_records.us.region_history.get_dates(),
            growth_rate=region_records.neighborhood.average_value_growth_rate,
            breadcrumbs=region_records.get_breadcrumbs()
        )
