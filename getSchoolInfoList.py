import requests
from db import mysqlConnection


class SchoolInfo:
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def get_list(self):
        idx = 1
        info = list()
        try:
            while True:
                response = requests.get(self.get_api_url(idx))
                response_data = response.json()
                for element in response_data["schoolInfo"][1]["row"]:
                    info.append(element)
                idx += 1
        except KeyError:
            return info

    def get_api_url(self, idx):
        base_url = "https://open.neis.go.kr"
        path = "/hub/schoolInfo"
        params = {
            "KEY": self.apiKey,
            "Type": "json",
            "pIndex": idx,
            "pSize": 1000,
            "SCHUL_KND_SC_NM": "고등학교"
        }

        uri = f"{base_url}{path}"
        response = requests.get(uri, params=params)
        return response.url
