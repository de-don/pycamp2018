import logging


def merge_dicts(d1, d2):
    """ Merge dicts d1 and d2. If key exists in d1 and d2,
    the value from the d1 will be used.

    Example:
        >> d1 = {"a": 1, "b":2}
        >> d2 = {"b": 3, "c":4}
        >> d3 = merge_dicts(d1, d2)
        >> d3
        {"a": 1, "b": 2, "c": 4}
    """

    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logger = logging.getLogger('merge_dicts')

    d3 = d1.copy()
    for key, value in d2.items():
        if d3.get(key, None):
            logger.warning('Key "%s" exists in both dicts. Value "%s" from d2 can be lost' % (key, value))
            pass
        else:
            d3.update({key: value})

    return d3
