import requests
from db import mysqlConnection


class SchoolInfo:
    def __init__(self, apiKey):
        self.apiKey = apiKey

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
            domain = element["HMPG_ADRES"] or ""
            location = element["ORG_RDNMA"] or ""

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
