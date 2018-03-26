import hashlib
from pathlib import Path


def get_file_hash(file_path):
    """ This function returns the SHA-1 hash of the file passed into it"""
    h = hashlib.sha1()

    # open file for reading in binary mode
    with file_path.open('rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


def file_data(item: Path):
    size = item.stat().st_size
    if size == 0:
        return None

    return get_file_hash(item), item


def recursion_finder(path):
    for item in path.iterdir():
        if item.is_dir():
            yield from recursion_finder(item)
            continue

        h = file_data(item)
        if h:
            yield h


if __name__ == '__main__':
    dir_path = Path('../')

    items = recursion_finder(dir_path)
    for file_hash, file_path in items:
        print(file_hash, file_path)
