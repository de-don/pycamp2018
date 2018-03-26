import hashlib
from collections import defaultdict
from pathlib import Path

import click

DELETE_TEXT = 'Enter number of files, separated by space, which you want to ' \
              'remove. Enter 0, for skip it.'
CONFIRM_TEXT = 'Delete?'

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


@click.command()
@click.argument('path_to_dir', type=click.Path(exists=True))
@click.option('-d', 'delete', is_flag=True, help="Show delete dialog?")
def find_copies(path_to_dir, delete):
    dir_path = Path(path_to_dir)

    files_iter = recursion_finder(dir_path)
    storage = defaultdict(list)

    # find all files and save his path and hash to dict.
    for file_hash, file_path in files_iter:
        storage[file_hash].append(file_path)

    # filter copies and unique files:
    copies = filter(lambda x: len(x[1]) > 1, storage.items())

    for sha1, files in copies:
        click.echo(f'Next files has sha1={sha1}:')
        for item_num, item in enumerate(files, 1):
            click.echo(f'    {item_num}) {item}.')

        if delete:
            while True:
                delete_nums = click.prompt(DELETE_TEXT, type=str, default=0)
                if delete_nums in [0, '0']:
                    break
                try:
                    delete_nums = delete_nums.split(" ")
                    delete_nums = map(str.strip, delete_nums)
                    delete_nums = map(int, delete_nums)
                except Exception as e:
                    print(e)
                    continue

                click.echo(f'Next files will be deleted:')
                for num in delete_nums:
                    item = files[num-1]
                    click.echo(f'    {item}')

                if click.confirm(CONFIRM_TEXT):
                    click.echo('Delete success!')
                    # Todo: delete
                else:
                    click.echo('Delete aborted!')

                break
        click.echo('='*20)



if __name__ == '__main__':
    find_copies()
