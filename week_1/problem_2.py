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

    for key, value in d2.items():
        if d1.get(key, None):
            logger.warning(f'Key "{key}" exists in both dicts. Value "{value}" from d2 can be lost')

    return {**d2, **d1}
