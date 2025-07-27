from dataclasses import dataclass, field
import requests
from services.config import AppSettings
from services.timers import APITimer
from typing import Dict, List
from urllib.parse import urljoin


config = AppSettings()

@dataclass
class APIResponse:
    data: List[Dict] = field(default_factory=list)
    execution_time: float = 0.0
    url: str = None
    success: bool = False
    status_code: int = 200
    request_type: str = "GET"
    error: Exception = None

    def __repr__(self):
        return f"""
            Data-Length: {len(self.data)}
            Execution-Time: {self.execution_time}
            Url: {self.url}
            Success: {self.success}
            Status-Code: {self.status_code}
            Request-Type: {self.request_type}
            Error: {self.error}
        """

def poll_api(url: str) -> APIResponse:

    timer = APITimer()
    result = APIResponse(request_type="GET", url=url)

    try:
        with timer:

            headers = {
                "User-Agent": "python-request/2.32.4",
            }

            response = requests.get(url, headers=headers)
            result.status_code = response.status_code

            if result.status_code == 200:
                result.data = response.json()
                result.success = True

    except Exception as ex:
        result.error = ex
        result.success = False
    finally:
        result.execution_time = timer.expired_milliseconds
        return result
    

class CBPCountyAPIClient:

    def poll(self, year: int):

        if year > 2016:
            url: str = f"https://api.census.gov/data/{year}/cbp?get=GEO_ID,ESTAB,PAYANN,PAYQTR1,EMP,NAICS2017&for=COUNTY:*&NAICS2017=*"
        else:
            url: str = f"https://api.census.gov/data/{year}/cbp?get=GEO_ID,ESTAB,PAYANN,PAYQTR1,EMP&for=COUNTY:*&NAICS2012=*"
        return poll_api(url)
    

class CBPStateAPIClient:

    def poll(self, year: int):

        if year > 2016:
            url: str = f"https://api.census.gov/data/{year}/cbp?get=GEO_ID,ESTAB,PAYANN,PAYQTR1,EMP,NAICS2017&for=STATE:*&NAICS2017=*"
        else:
            url: str = f"https://api.census.gov/data/{year}/cbp?get=GEO_ID,ESTAB,PAYANN,PAYQTR1,EMP,NAICS2012&for=STATE:*&NAICS2012=*"

        return poll_api(url)

