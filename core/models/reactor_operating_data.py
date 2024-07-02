from dataclasses import dataclass
from datafiles import datafile
from datetime import datetime
from requests_cache import CachedSession
from datetime import datetime, timedelta, UTC
from bs4 import BeautifulSoup

@dataclass
class ReactorOperatingDataPoint:
    timestamp: datetime
    value_MW: float
    value_percent: float

@datafile("../data/reactor_operating_data/{self.reactor_label}.yml")
class ReactorOperatingData:
    reactor_label: str
    reactor_name: str
    reactor_type: str
    index_in_data: int
    url: str
    data_points: list[ReactorOperatingDataPoint]

    def get_reactor_data(self):
        session = CachedSession('reactor_operating_data', expire_after=timedelta(minutes=0.2))
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'}

        page = session.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        script = soup.select("body > section > script:nth-child(2)")
        timestamp = datetime.fromtimestamp(int(script[0].string.split("timestamp\\\":")[1].split(",")[0]) / 1000.0, UTC)
        value_MW = float(script[0].string.split("production\\\":")[self.index_in_data].split(",")[0])
        value_percent = float(script[0].string.split("percent\\\":")[self.index_in_data].split("}")[0])
        
        return ReactorOperatingDataPoint(timestamp, value_MW, value_percent)

    def timestamp_is_present(self, timestamp):
        for data_point in self.data_points:
            if data_point.timestamp == timestamp:
                return True
        return False
    

