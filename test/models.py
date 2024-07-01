from dataclasses import dataclass
from datafiles import datafile, converters
from datetime import datetime, timezone

@dataclass
class DataPoint:
    timestamp: datetime
    value_MW: float
    value_percent: float

@datafile("data/{self.reactor_label}.yml")
class StoredReactorData:
    reactor_label: str
    data_points: list[DataPoint]

    def timestamp_is_present(self, timestamp):
        for data_point in self.data_points:
            if data_point.timestamp == timestamp:
                return True
        return False
    

# Based on https://datafiles.readthedocs.io/en/latest/types/custom/
class DateTimeConverter(converters.Converter):
    @classmethod
    def to_preserialization_data(cls, python_value: datetime, **kwargs):
        # Convert `datetime` to a value that can be serialized
        return python_value.isoformat()

    @classmethod
    def to_python_value(cls, deserialized_data: str, **kwargs):
        # Convert file value back into a `datetime` object
        return datetime.fromisoformat(deserialized_data)

converters.register(datetime, DateTimeConverter)

# Based on https://stackoverflow.com/a/13287083
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)