from datetime import datetime


def format_datetime(value: datetime | None, date_format: str = "european") -> str:
    """"""

    value_str = ""

    if value is None:
        return value_str

    elif date_format == "british":
        return value.strftime("%A, %d de %b de %Y")

    elif date_format == "european":
        return value.strftime("%d/%m/%Y")

    else:
        return value.strftime("%d-%m-%YT%H:%M:%S")
