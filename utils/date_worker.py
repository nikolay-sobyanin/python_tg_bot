from config_data.config import FORMAT_DATE
from datetime import date, datetime, timedelta


def get_date_obj(date_str: str) -> date:
    return datetime.strptime(date_str, FORMAT_DATE).date()


def get_date_str(date_obj: date, format_date=FORMAT_DATE) -> str:
    return date_obj.strftime(format_date)


def get_today() -> date:
    return date.today()


def get_delta_date(days: int, start_date=get_today()) -> date:
    return start_date + timedelta(days=days)
