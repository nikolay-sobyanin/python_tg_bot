from loguru import logger

my_logger = logger


def info_only(record) -> bool:
    return record['level'].name == 'INFO'


my_logger.add('utils/logging/info.log', format='{time} | {level} | {message}', level='INFO', rotation='1 week',
              compression='zip', filter=info_only)
my_logger.add('utils/logging/error.log', format='{time} | {level} | {message}', level='ERROR', rotation='1 week',
              compression='zip')
