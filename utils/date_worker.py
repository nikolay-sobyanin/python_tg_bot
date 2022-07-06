from config_data.config import FORMAT_DATE
from datetime import date, datetime, timedelta


def get_date_obj(date_str: str) -> date:
    return datetime.strptime(date_str, FORMAT_DATE).date()


def get_date_str(date_obj: date, format_date=FORMAT_DATE) -> str:
    return date_obj.strftime(format_date)


def get_date_time_str(date_time: datetime) -> str:
    return date_time.strftime('%d.%m.%Y %H:%M:%S')


def get_today() -> date:
    return date.today()


def get_delta_date(days: int, start_date=get_today()) -> date:
    return start_date + timedelta(days=days)


def get_count_days(start_date: str, end_date: str) -> int:
    date_from = datetime.strptime(start_date, FORMAT_DATE).date()
    date_to = datetime.strptime(end_date, FORMAT_DATE).date()
    return (date_to - date_from).days
