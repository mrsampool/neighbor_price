class RegionLink:
    def __init__(self, label: str, region_id: str):
        self.label = label
        self.region_id: str = region_id
        self.address: str = self.get_address()

    def get_address(self):
        raise NotImplementedError


class USLink(RegionLink):

    def __init__(self):
        super().__init__(label="USA", region_id="")

    def get_address(self):
        return f"/"


class StateLink(RegionLink):

    def __init__(self, label: str, region_id: str):
        super().__init__(label=label, region_id=region_id)

    def get_address(self):
        return f"/state/{self.region_id}"


class MetroLink(RegionLink):

    def __init__(
            self,
            label: str,
            region_id: str,
            state_id: str
    ):
        self.state_id = state_id
        super().__init__(label=label, region_id=region_id)

    def get_address(self):
        return f"/state/{self.state_id}/metro/{self.region_id}"


class CityLink(RegionLink):

    def __init__(
            self,
            label: str,
            region_id: str,
            state_id: str,
            metro_id: str
    ):
        self.metro_id = metro_id
        self.state_id = state_id
        super().__init__(label=label, region_id=region_id)

    def get_address(self):
        return f"/state/{self.state_id}/metro/{self.metro_id}/city/{self.region_id}"


class NeighborhoodLink(RegionLink):

    def __init__(
            self,
            label: str,
            region_id: str,
            state_id: str,
            metro_id: str,
            city_id: str
    ):
        self.metro_id = metro_id
        self.state_id = state_id
        self.city_id = city_id
        super().__init__(label=label, region_id=region_id)

    def get_address(self):
        return f"/state/{self.state_id}/metro/{self.metro_id}/city/{self.city_id}/neighborhood/{self.region_id}"