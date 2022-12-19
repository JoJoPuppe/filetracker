from datetime import datetime

def parse_rfc3339(datetime_str: str) -> datetime:
    try:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        # Perhaps the datetime has a whole number of seconds with no decimal
        # point. In that case, this will work:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")

def convert_date(iso_date):
    date_obj = parse_rfc3339(iso_date)
    return datetime.strftime(date_obj, "%d.%m.%y | %H:%M:%S")
