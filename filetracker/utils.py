from datetime import datetime

def parse_rfc3339(datetime_str: str) -> datetime:
    try:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        # Perhaps the datetime has a whole number of seconds with no decimal
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
        # point. In that case, this will work:
        # 2022-11-29T10:14:53.499777
            return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")

def convert_date(iso_date):
    date_obj = parse_rfc3339(iso_date)
    print(date_obj)
    return datetime.strftime(date_obj, "%d.%m.%y | %H:%M:%S")
