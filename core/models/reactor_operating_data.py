from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from bs4 import BeautifulSoup
from datafiles import datafile
from requests_cache import CachedSession


@dataclass
class ReactorOperatingDataPoint:
    timestamp: datetime
    mw: float
    pct: float


@datafile("../data/reactor_operating_data/{self.reactor_label}.yml")
class ReactorOperatingData:
    reactor_label: str
    reactor_name: str
    reactor_type: str
    index_in_json_list: int
    index_in_data: int
    url: str

    def get_reactor_data(self):
        session = CachedSession(
            "reactor_operating_data", expire_after=timedelta(minutes=0.2)
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
        }

        page = session.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        script_tags_with_json = soup.find_all("script", {"type": "application/json"})
        json_contents = [tag.string for tag in script_tags_with_json]
        json_content = json_contents[self.index_in_json_list]
        timestamp = datetime.fromisoformat(
            json_content.split('timestamp":')[1].split(",")[0].strip('"')
        )
        mw = float(json_content.split('production":')[self.index_in_data].split(",")[0])
        pct = float(json_content.split('percent":')[self.index_in_data].split("}")[0])

        # Round the values
        mw = round(mw, 1)
        pct = round(pct, 1)

        return ReactorOperatingDataPoint(timestamp, mw, pct)
