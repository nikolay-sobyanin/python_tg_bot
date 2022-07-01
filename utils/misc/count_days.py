from datetime import datetime
from config_data.config import FORMAT_DATE


def get_count_days(check_in, check_out):
    date_from = datetime.strptime(check_in, FORMAT_DATE).date()
    date_to = datetime.strptime(check_out, FORMAT_DATE).date()
    return (date_to - date_from).days
