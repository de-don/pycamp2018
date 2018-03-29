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


def get_url_pattern(url):
    matches = re.finditer(r'([^/]+)/(\d+)/', url)
    params = {}
    for match in matches:
        name, value = match.groups()
        params[name] = value

    pattern = re.sub(r'([^/]+)/(\d+)/', r'\1/<\1-id>/', url)
    return pattern, params


def get_url_patterns(url_patterns):
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
    log = matchobj.groupdict()
    log['headers'] = json.loads(log['headers'])
    log['query'] = json.loads(log['query'])
    log['url_pattern'], log['url_params'] = get_url_pattern(log['url'])
    return log


matches = re.finditer(pattern, data, flags=re.DOTALL)
logs = [match_to_dict(match) for match in matches]
pprint(logs)

input("press key...")
urls_dict = get_url_patterns(map(itemgetter('url_pattern'), logs))
pprint(urls_dict)
