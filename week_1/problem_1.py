from collections import Counter
from typing import List


def sum_of_keys(list_of_dicts: List[dict]) -> List[dict]:
    """ Function to calc and return count keys in dicts with equal values

    Args:
        list_of_dicts(List[dict]): list with some dicts

    Returns:
        List[dict]: list with dicts, when each dict have this structure:
            {'key': key_name, 'value': key_value, 'count': count_items}

    """

    counter = Counter()
    # add to counter items from each dict
    for one_dict in list_of_dicts:
        counter.update(one_dict.items())

    for item, count in counter.items():
        yield {'key': item[0], 'value': item[1], 'count': count}
