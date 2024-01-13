from dataclasses import dataclass

import pandas as pd


@dataclass
class MockResponse:
    content: bytes


def mocked_requests_get(*args, **kwargs) -> MockResponse:

    def dict_to_encoded_csv(dict_data: dict) -> bytes:
        df = pd.DataFrame(dict_data)
        csv_string = df.to_csv(index=False)
        return csv_string.encode('utf-8')

    match args[0]:
        case 'csv/neighborhoods':
            content = dict_to_encoded_csv({
                "RegionId": ["region-id-1"],
                "SizeRank": ["size-1"],
                "RegionName": ["region-1"],
                "RegionType": ["neighborhood"],
                "StateName": ["state-1"],
                "State": ["state-1"],
                "City": ["city-1"],
                "Metro": ["metro-1"],
                "CountyName": ["county-1"],
                "2000-01-31": [100],
                "2000-02-20": [200]
            })
            return MockResponse(content=content)