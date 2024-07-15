import threading
from .every import every

import time
from datafiles import Missing
import http.client

from models import datetime_converter
from models.reactor_operating_data import ReactorOperatingData
from time_series_data.reactor_operating_data import add_reactor_operating_data_point, point_is_present

def fetch_reactor_operating_data():
    print("Fetching reactor operating data 🕒")
    for reactor in ReactorOperatingData.objects.all():
        reactor: ReactorOperatingData
        try:
            reactor_data = reactor.get_reactor_data()
            print(f"{reactor.reactor_name}: {datetime_converter.utc_to_local(reactor_data.timestamp)}, {reactor_data.mw:.0f} MW, {reactor_data.pct:.1f} %")

            if not point_is_present(reactor, reactor_data):
                add_reactor_operating_data_point(reactor, reactor_data)
                print(f"Added datapoint 🟢")
            else:
                print(f"Datapoint present 🔵")

        except http.client.RemoteDisconnected as e:
            print(f"Datapoint not added 🔴")
            print(f"Error: {e}")

threading.Thread(target=lambda: every(5*60, fetch_reactor_operating_data)).start()