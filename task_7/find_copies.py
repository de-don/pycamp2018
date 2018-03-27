import hashlib
from pathlib import Path

import click
from funcy import group_by, select_keys

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
    """ This function returns the SHA-1 hash of the file

    Args:
        file_path(PurePath): path to file

    Returns:
        str: sha1 hash of file content

    """
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


def get_file_size(file_path):
    """ Return size of file.

    Args:
        file_path(PurePath): path to file

    Return:
        int: size of file

    """
    return file_path.stat().st_size


def recursion_finder(path):
    """ Recursion generator to find all files in directory

    Args:
        path(PurePath): path to directoey

    Yields:
        PurePath: files in directory or sub-directory's

    """

    for item in path.iterdir():
        if item.is_dir():
            yield from recursion_finder(item)
            continue
        if item.exists():
            yield item


def process_str_of_nums(numbers, range_num=None):
    """ Convert string with nums sep by spases to int's

    Args:
        numbers(str): numbers separated by space.
        range_num(seq): pair of min and max allowed number.

    Yields:
        int: number from numbers string.

    Raises:
        IndexError: if numbers not in range_num

    """

    for num in numbers.split(" "):
        num = int(num.strip())

        if not range_num:
            yield num
            continue
        if range_num[0] > num or num > range_num[1]:
            raise IndexError(f'Index {num} out of range {range_num}')
        yield num


def sha1_copies(file_sizes):
    """ Find files identical by size and sha1.

    Get on input files combined in pairs by size: (size, list_of_files)

    Args:
        file_sizes(List[tuple]): pairs (size, files), where files it is
            list of PurePath files with file_size = size.

    Yields:
        list: lists of files identical by sha1 and size
    """
    for size, files in file_sizes:
        file_hashes = group_by(get_file_sha1, files)

        # yield list of files with same sha1
        for sha1, copy_files in file_hashes.items():
            if len(copy_files) > 1:
                yield copy_files


@click.command()
@click.argument('path_to_dir', type=click.Path(exists=True))
@click.option('-d', 'delete', is_flag=True, help=TEXTS['help_delete'])
def find_copies(path_to_dir, delete):
    dir_path = Path(path_to_dir)

    dir_iter = recursion_finder(dir_path)

    file_sizes = group_by(get_file_size, dir_iter)
    file_sizes = select_keys(None, file_sizes)

    # view copies grouped by sha1
    for copies in sha1_copies(file_sizes.items()):
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
                # user input wrong format. View error and back to input numbers
                click.echo(f'Error: {exp}')
                continue

            # if users choice not delete files
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
