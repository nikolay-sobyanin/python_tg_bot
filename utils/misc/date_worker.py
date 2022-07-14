from config_data.config import FORMAT_DATE
from datetime import date, datetime, timedelta


class DateWorker:

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def today() -> date:
        return date.today()

    @staticmethod
    def date_obj(enter_date: str) -> date:
        return datetime.strptime(enter_date, FORMAT_DATE).date()

    @staticmethod
    def date_str(enter_date: date, format_date=FORMAT_DATE) -> str:
        return enter_date.strftime(format_date)

    @staticmethod
    def date_time_str(date_time: datetime) -> str:
        return date_time.strftime('%d.%m.%Y %H:%M:%S')

    @staticmethod
    def date_delta(days_delta: int, start_date=today()) -> date:
        return start_date + timedelta(days=days_delta)

    @staticmethod
    def count_days(start_date: str, end_date: str) -> int:
        date_from = datetime.strptime(start_date, FORMAT_DATE).date()
        date_to = datetime.strptime(end_date, FORMAT_DATE).date()
        return (date_to - date_from).days
