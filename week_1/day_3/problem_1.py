from collections import Counter


def gen_item(item, count):
    """ Create dict for item with its frequency """
    return {"key": item[0], "value": item[1], "count": count}


def sum_of_keys(list_of_dicts):
    """ Function to calculate and return count keys in dicts with equal values """
    counter = Counter()

    # add to counter items from each dict
    for one_dict in list_of_dicts:
        counter.update(one_dict.items())

    return [gen_item(item, count) for item, count in counter.items()]
