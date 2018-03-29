import json
import re
from pprint import pprint

data = None

with open('data.log', 'r') as f:
    data = f.read()

pattern = r'(?P<date>\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2},\d{1,4}) ' \
          r'middleware (?P<method>GET|POST) (?P<url>.*?) => (?P<status>\d+)\n' \
          r'Query:\n(?P<query>{.*?})\nHeaders:\n(?P<headers>{.*?})'


def match_to_dict(matchobj):
    log = matchobj.groupdict()
    log['headers'] = json.loads(log['headers'])
    log['query'] = json.loads(log['query'])
    return log


matches = re.finditer(pattern, data, flags=re.DOTALL)

logs = [match_to_dict(match) for match in matches]

pprint(logs)
