from tinyflux import TagQuery, TimeQuery, TinyFlux, Point
from datetime import datetime

from models.reactor_operating_data import ReactorOperatingData, ReactorOperatingDataPoint

db = TinyFlux('data/reactor_operating_data/tinyflux.csv')

def add_reactor_operating_data_point(reactor_operating_data: ReactorOperatingData, point: ReactorOperatingDataPoint):
    p = Point(
        measurement="P",
        time=point.timestamp,
        tags={"RX": reactor_operating_data.reactor_label},
        fields={"mw": point.mw, "pct": point.pct}
    )

    db.insert(p, compact_key_prefixes=True)

def point_is_present(reactor_operating_data: ReactorOperatingData, point: ReactorOperatingDataPoint):
    Time = TimeQuery()
    Tag = TagQuery()
    q1 = Time == point.timestamp
    q2 = Tag.RX == reactor_operating_data.reactor_label

    return db.contains(q1 & q2)

def get_points_between_dates(reactor_operating_data: ReactorOperatingData, start: datetime = None, stop: datetime = None):
    Time = TimeQuery()
    Tag = TagQuery()
    q = Tag.RX == reactor_operating_data.reactor_label
    if start:
        q = q & (Time >= start)
    if stop:
        q = q & (Time <= stop)

    return db.search(q)
    
def get_start_stop_intervals():
    timestamps = db.get_timestamps()

    start: datetime = min(timestamps)
    stop: datetime = max(timestamps)

    return start, stop