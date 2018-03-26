import hashlib
from collections import defaultdict
from pathlib import Path

import click

TEXTS = {
    'identical_files': 'Next files are identical:',
    'delete': 'Enter number of files, separated by space, which you'
              ' want to remove. Enter 0, for skip it.',
    'confirm': 'Really delete?',
    'delete_list': 'Next files will be deleted:',
    'delete_success': 'Delete success!',
    'delete_aborted': 'Delete aborted!',
    'help_delete': 'Show delete dialog?',
}


def get_file_hash(file_path):
    """ This function returns the SHA-1 hash of the file """
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


def file_data(item):
    """ Function to get file sha1, if file not empty, else None"""
    size = item.stat().st_size
    if size == 0:
        return None
    return get_file_hash(item), item


def recursion_finder(path):
    """ Recursion generator to find all not_empty files and get his sha1 """
    for item in path.iterdir():
        if item.is_dir():
            yield from recursion_finder(item)
            continue

        h = file_data(item)
        if h:
            yield h


def process_str_of_nums(numbers, range_num=None):
    for num in numbers.split(" "):
        num = int(num.strip())

        if not range_num:
            yield num
            continue
        if range_num[0] > num  or num > range_num[1]:
            raise IndexError(f'Index {num} out of range {range_num}')
        yield num


@click.command()
@click.argument('path_to_dir', type=click.Path(exists=True))
@click.option('-d', 'delete', is_flag=True, help=TEXTS['help_delete'])
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
        click.echo(TEXTS['identical_files'])
        for item_num, item in enumerate(files, 1):
            click.echo(f'    {item_num}) {item}.')

        if not delete:
            continue

        while True:
            # wait user input
            users_input = click.prompt(TEXTS['delete'], default='0')
            try:
                nums = process_str_of_nums(users_input, [0, len(files)])
                nums = list(nums)
            except Exception as exp:
                click.echo(f'Error: {exp}')
                continue

            if 0 in nums:
                break

            # show files to delete
            click.echo(TEXTS['delete_list'])
            for num in nums:
                item = files[num - 1]
                click.echo(f'    {item}')

            if click.confirm(TEXTS['confirm']):
                click.echo(TEXTS['delete_success'])
                # Todo: delete
            else:
                click.echo(TEXTS['delete_aborted'])

            break
        click.echo('=' * 20)


if __name__ == '__main__':
    find_copies()
