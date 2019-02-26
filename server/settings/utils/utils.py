
import logging

# Get an instance of a logger
logger = logging.getLogger("django")


def parse_db_variable(var_string):
    import re

    if not var_string:
        return []

    regex = r'.*\/\/(\w+):(\w+)@([A-Za-z0-9\-\.]+):(\d{4})\/(\w+)'

    logger.info("Parse db variable: {}".format(var_string))
    m = re.match(regex, var_string)
    if m:
        return m.groups()
    return list()