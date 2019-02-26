def parse_db_variable(var_string):
    import re
    regex = r"\/\/(\w+):(\w+)@([A-Za-z0-9\-\.]+):(\d{4})\/(\w+)"

    groups = list()
    m = re.match(regex, var_string)
    if m:
        for groupNum in range(0, len(m.groups())):
            groups.append(m.group(groupNum))
    return groups