import requests
from db import mysqlConnection
from urllib.parse import urlparse


class SchoolInfo:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.location = ""

    def save_data(self):
        conn = mysqlConnection.connection_pool
        cursor = conn.cursor()

        school_list = self.get_list()

        delete_query = "delete from school"
        cursor.execute(delete_query)

        for element in school_list:
            office_code = element["ATPT_OFCDC_SC_CODE"] or ""
            code = element["SD_SCHUL_CODE"] or ""
            name = element["SCHUL_NM"] or ""
            location = self.get_sliced_location(element["ORG_RDNMA"] or "")
            self.location = location

            if name == "경북나이스고등학교(교육용)":
                continue

            domain = self.get_sliced_domain(element.get("HMPG_ADRES", ""))

            insert_query = "insert into school(school_id, school_name, school_domain, school_location, school_office_code) values(%s, %s, %s, %s, %s)"
            insert_values = (code, name, domain, location, office_code)

            cursor.execute(insert_query, insert_values)

        conn.commit()
        conn.close()

        print("Success!!")

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

    def get_sliced_location(self, location: str):
        location = location.strip()
        location = location.replace("  ", " ")
        state, city = location.split(" ")[0], location.split(" ")[1]

        if "광역시" in state:
            state = state.replace("광역시", "")
        elif "특별" in state:
            if "특별자치시" in state:
                state = state.replace("특별자치시", "")
            elif "특별자치도" in state:
                state = state.replace("특별자치", "")
            elif "특별시" in state:
                state = state.replace("특별시", "")
        elif len(state) == 4:
            location = list(state)
            state = location[0] + location[2]

        return state + " " + city

    def get_sliced_domain(self, domain):
        url = urlparse(domain)

        if self.location.split(" ")[0] == "경북" or "school.gyo6.net" in str(url.netloc + url.path):
            sliced_url = str(url.netloc + url.path)
        elif not bool(url.scheme):
            sliced_url = str(url.path)
        else:
            sliced_url = str(url.netloc)

        if "www." in sliced_url:
            sliced_url = sliced_url.replace("www.", "")

        return sliced_url
