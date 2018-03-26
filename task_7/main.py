import hashlib
from collections import defaultdict
from pathlib import Path

import click

TEXTS = {
    'identical_files': 'Next files are identical:',
    'delete': 'Enter number of files, separated by space, which you'
              ' want to remove. Enter 0, to skip it.',
    'confirm': 'Really delete?',
    'delete_list': 'Next files will be deleted:',
    'delete_success': 'Delete success!',
    'delete_aborted': 'Delete aborted!',
    'help_delete': 'Show delete dialog?',
}


def get_file_sha1(file_path):
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


def non_empty_files(iter_files):
    for file in iter_files:
        size = file.stat().st_size
        if size:
            yield size, file

def recursion_finder(path):
    """ Recursion generator to find all files """
    for item in path.iterdir():
        if item.is_dir():
            yield from recursion_finder(item)
            continue
        yield item


def process_str_of_nums(numbers, range_num=None):
    for num in numbers.split(" "):
        num = int(num.strip())

        if not range_num:
            yield num
            continue
        if range_num[0] > num or num > range_num[1]:
            raise IndexError(f'Index {num} out of range {range_num}')
        yield num


def sha1_copies(file_sizes):
    file_hashes = defaultdict(list)
    for _, files in file_sizes.items():
        file_hashes.clear()

        for file in files:
            sha1 = get_file_sha1(file)
            file_hashes[sha1].append(file)

        for sha1, copy_files in file_hashes.items():
            if len(copy_files) > 1:
                yield copy_files



@click.command()
@click.argument('path_to_dir', type=click.Path(exists=True))
@click.option('-d', 'delete', is_flag=True, help=TEXTS['help_delete'])
def find_copies(path_to_dir, delete):
    dir_path = Path(path_to_dir)

    dir_iter = recursion_finder(dir_path)
    files_data_iter = non_empty_files(dir_iter)

    file_sizes = defaultdict(list)
    # find all files and save his path and hash to dict.
    for file_size, file_path in files_data_iter:
        file_sizes[file_size].append(file_path)

    for copies in sha1_copies(file_sizes):
        click.echo(TEXTS['identical_files'])
        for item_num, item in enumerate(copies, 1):
            click.echo(f'    {item_num}) {item}.')

        if not delete:
            continue

        while True:
            # wait user input
            users_input = click.prompt(TEXTS['delete'], default='0')
            try:
                nums = process_str_of_nums(users_input, [0, len(copies)])
                nums = list(nums)
            except Exception as exp:
                click.echo(f'Error: {exp}')
                continue

            if 0 in nums:
                break

            delete_files = [copies[num - 1] for num in nums]

            # show files to delete
            click.echo(TEXTS['delete_list'])
            for file in delete_files:
                click.echo(f'    {file}')

            if click.confirm(TEXTS['confirm']):
                for file in delete_files:
                    Path.unlink(file)
                click.echo(TEXTS['delete_success'])
            else:
                click.echo(TEXTS['delete_aborted'])

            break
        click.echo('=' * 20)


if __name__ == '__main__':
    find_copies()
