import threading
from .every import every

import time
from datafiles import Missing
import http.client

from models import datetime_converter
from models.reactor_operating_data import ReactorOperatingData

def fetch_reactor_operating_data():
    print("Fetching reactor operating data 🕒")
    for reactor in ReactorOperatingData.objects.all():
        reactor: ReactorOperatingData
        try:
            reactor_data = reactor.get_reactor_data()
            print(f"{reactor.reactor_name}: {datetime_converter.utc_to_local(reactor_data.timestamp)}, {reactor_data.value_MW:.0f} MW, {reactor_data.value_percent:.1f} %")

            if reactor.data_points == Missing:
                print(f"Data points missing ⚫️")
                reactor.data_points = []

            if not reactor.timestamp_is_present(reactor_data.timestamp):
                print(f"Added datapoint 🟢")
                reactor.data_points.append(reactor_data)
            else:
                print(f"Datapoint present 🔵")

        except http.client.RemoteDisconnected as e:
            print(f"Datapoint not added 🔴")
            print(f"Error: {e}")

threading.Thread(target=lambda: every(5*60, fetch_reactor_operating_data)).start()