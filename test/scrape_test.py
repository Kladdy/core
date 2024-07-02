from bs4 import BeautifulSoup
from dataclasses import dataclass
from requests_cache import CachedSession
from datetime import datetime, timedelta, UTC
import time
from datafiles import Missing
import http.client
from datafiles import datafile

from models import DataPoint, StoredReactorData, utc_to_local

# Or use timedelta objects to specify other units of time
session = CachedSession('vattenfall_reactors_cache', expire_after=timedelta(minutes=0.2))
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'}

@datafile("data/config_data/{self.label}.yml")
class Reactor:
    name: str
    label: str
    index_in_data: int
    url: str

    def get_reactor_data(self):
        page = session.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        script = soup.select("body > section > script:nth-child(2)")
        timestamp = datetime.fromtimestamp(int(script[0].string.split("timestamp\\\":")[1].split(",")[0]) / 1000.0, UTC)
        value_MW = float(script[0].string.split("production\\\":")[self.index_in_data].split(",")[0])
        value_percent = float(script[0].string.split("percent\\\":")[self.index_in_data].split("}")[0])
        return DataPoint(timestamp, value_MW, value_percent)

reactors : list[Reactor] = [
    Reactor("Forsmark 1", "F1", 1, "https://gvp.vattenfall.com/sweden/produced-power/iframe/forsmark"),
    Reactor("Forsmark 2", "F2", 2, "https://gvp.vattenfall.com/sweden/produced-power/iframe/forsmark"),
    Reactor("Forsmark 3", "F3", 3, "https://gvp.vattenfall.com/sweden/produced-power/iframe/forsmark"),
    Reactor("Ringhals 3", "R3", 1, "https://gvp.vattenfall.com/sweden/produced-power/iframe/ringhals"),
    Reactor("Ringhals 4", "R4", 2, "https://gvp.vattenfall.com/sweden/produced-power/iframe/ringhals"),
]

def main():
    for reactor in reactors:
        reactor_data = reactor.get_reactor_data()
        print(f"{reactor.name}: {utc_to_local(reactor_data.timestamp)}, {reactor_data.value_MW:.0f} MW, {reactor_data.value_percent:.1f} %")

        if reactor_data.value_percent == 0:
            print(f"\t{reactor.name} is not producing power")
        else:
            print(f"\tAccording to this data, the maximum power output of {reactor.name} is {(reactor_data.value_MW / (reactor_data.value_percent / 100)):.0f} MW")

        data = StoredReactorData(reactor.label, Missing)
        if data.data_points == Missing:
            data.data_points = []

        if not data.timestamp_is_present(reactor_data.timestamp):
            print(f"👍")
            data.data_points.append(reactor_data)
        else:
            print(f"👎")

if __name__ == "__main__":
    while True:
        try:
            main()
        except http.client.RemoteDisconnected as e:
            print(f"Error: {e}")
        print("Sleeping for 5 minutes")
        time.sleep(300)