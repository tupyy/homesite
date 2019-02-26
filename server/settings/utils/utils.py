
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def parse_db_variable(var_string):
    import re

    if not var_string:
        return []

    regex = r'\/\/(\w+):(\w+)@([A-Za-z0-9\-\.]+):(\d{4})\/(\w+)'

    logger.info("Parse db variable: {}".format(var_string))
    groups = list()
    p = re.compile(regex)
    m = p.match(regex, var_string)
    if m:
        for groupNum in range(0, len(m.groups())):
            logger.info('Var: {}'.format(m.group(groupNum)))
            groups.append(m.group(groupNum))
    return groups