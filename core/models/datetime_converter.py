# Based on https://datafiles.readthedocs.io/en/latest/types/custom/
from datafiles import converters
from datetime import datetime, timezone

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
def utc_to_local(utc_dt: datetime):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)