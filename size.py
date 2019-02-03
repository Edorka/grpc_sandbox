class SIZE:

    KB = 1024
    MB = 1024 * KB
    GB = 1024 * MB
    TB = 1024 * GB


def extract(size, unit_size):
    return int(size / unit_size)


def bytes_to_human(size):
    if size < SIZE.KB:
        return "{}B".format(size)
    if size < SIZE.MB:
        return "{}Kb".format(extract(size, SIZE.KB))
    if size < SIZE.GB:
        return "{}Mb".format(extract(size, SIZE.MB))
    if size < SIZE.TB:
        return "{}Gb".format(extract(size, SIZE.GB))
    return "{}Tb".format(extract(size, SIZE.TB))
