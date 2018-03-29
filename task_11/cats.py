import hashlib
import re
from random import randint

import requests

path = './tmp/{}_{}.jpg'


def get_urls(count):
    url_xml = f'http://thecatapi.com/api/images/get?format=xml&results_per_page={count}'
    res = requests.get(url_xml)
    cat_urls = re.findall(r'<url>\s*(.*?)\s*</url>', res.text)
    return cat_urls


def save_cat_and_print_hash(name, url):
    r = requests.get(url)
    if r.status_code != 200:
        print('error')
        return

    path_img = path.format(randint(0, 10 ** 5), randint(0, 10 ** 5))
    with open(path_img, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    with open(path_img, 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        print(name, m.hexdigest())
