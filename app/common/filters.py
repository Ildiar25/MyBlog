import base64
from datetime import datetime
from babel.dates import format_datetime


def give_format_to_date(value: datetime | None, date_format: str = "european") -> str:
    """"""

    value_str = ""

    if value is None:
        return value_str

    elif date_format == "british":
        return format_datetime(value, format="EEEE, dd 'de' MMMM 'de' yyyy", locale="es").capitalize()

    elif date_format == "european":
        return format_datetime(value, format="dd/MM/yy, HH:mm", locale="es")

    elif date_format == "url":
        return base64.urlsafe_b64encode(value.strftime("%d-%m-%YT%H:%M:%S").encode()).decode()

    else:
        return format_datetime(value, format="dd-MM-yyyy'T'HH:mm:ssZ", locale="es")
