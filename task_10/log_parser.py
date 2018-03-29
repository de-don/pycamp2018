import json
import re
from operator import itemgetter
from pprint import pprint

data = None

with open('data.log', 'r') as f:
    data = f.read()

pattern = r'(?P<date>\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2},\d{1,4}) ' \
          r'middleware (?P<method>GET|POST) (?P<url>.*?) => (?P<status>\d+)\n' \
          r'Query:\n(?P<query>{.*?})\nHeaders:\n(?P<headers>{.*?})'


def get_url_info(url):
    """ Function to get info by url: url pattern and current url params.

    Args:
        url(str): url-adress, for example "/api/v1/post/123/delete"

    Returns:
        str: url-pattern, for example "/api/v1/post/<post-id>/delete"
        dict: url parameters, for example {'post-id': 123}
    """
    matches = re.finditer(r'([^/]+)/(\d+)/', url)
    params = {}
    for match in matches:
        name, value = match.groups()
        params[name] = value

    pattern = re.sub(r'([^/]+)/(\d+)/', r'\1/<\1-id>/', url)
    return pattern, params


def get_url_patterns(url_patterns):
    """ Function to get more-dimensional dict where each way it is pattern. """
    dictionary = {}
    for url in url_patterns:
        url = url.split("/")[1:-1]
        curr_dict = dictionary
        for i, part in enumerate(url):
            if part not in curr_dict:
                curr_dict[part] = {}
            curr_dict = curr_dict[part]
    return dictionary


def match_to_dict(matchobj):
    """ Transform match object of one log-node to log-dictionary """
    log = matchobj.groupdict()
    log['headers'] = json.loads(log['headers'])
    log['query'] = json.loads(log['query'])
    log['url_pattern'], log['url_params'] = get_url_info(log['url'])
    return log


matches = re.finditer(pattern, data, flags=re.DOTALL)
logs = [match_to_dict(match) for match in matches]
pprint(logs)

input("press key...")
urls_dict = get_url_patterns(map(itemgetter('url_pattern'), logs))
pprint(urls_dict)
