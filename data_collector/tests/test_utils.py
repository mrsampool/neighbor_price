from dataclasses import dataclass

import pandas as pd


@dataclass
class MockResponse:
    content: bytes


def dict_to_encoded_csv(dict_data: dict) -> bytes:
    df = pd.DataFrame(dict_data)
    csv_string = df.to_csv(index=False)
    return csv_string.encode('utf-8')
