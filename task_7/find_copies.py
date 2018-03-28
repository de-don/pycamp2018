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


def sha1_copies(files):
    """ Find files identical sha1.

    Args:
        files(Iterable[PurePath]): Iterable of files.

    Yields:
        list: lists of files identical by sha1
    """
    file_hashes = group_by(get_file_sha1, files)

    for sha1, copy_files in file_hashes.items():
        if len(copy_files) > 1:
            yield copy_files


def sha1_copies_from_groups(groups_files):
    """ Generator for get groups of copies in each group in groups_files. """
    for files in groups_files:
        yield from sha1_copies(files)


def delete_files(files):
    """ Function to remove files """
    for file in files:
        Path.unlink(file)


def not_alone_item(items):
    """ Function to check that items it is not single item  """
    return len(items) > 1


##############################################################
# User interface
##############################################################

def show_list_files(files, text):
    """ Show list of files with description `text`. """

    click.echo(text)
    for item_num, item in enumerate(files, 1):
        click.echo(f'    {item_num}) {item}')


def get_nums_for_delete(files):
    while True:
        users_input = click.prompt(TEXTS['delete'], default='0')
        try:
            nums = process_str_of_nums(users_input, [0, len(files)])
            nums = list(nums)
        except Exception as exp:
            # user input wrong format. View error and back to input numbers
            click.echo(f'Error: {exp}')
            continue
        return nums


@click.command()
@click.argument('path_to_dir', type=click.Path(exists=True))
@click.option('-d', 'delete', is_flag=True, help=TEXTS['help_delete'])
def find_copies(path_to_dir, delete):
    dir_path = Path(path_to_dir)

    dir_iter = recursion_finder(dir_path)
    # group all files by size and filter 0-sized files
    file_sizes = group_by(get_file_size, dir_iter)
    file_sizes = select_keys(None, file_sizes)
    # get groups of files and filter one-members groups
    files_groups = filter(not_alone_item, file_sizes.values())

    # view copies grouped by sha1
    for copies in sha1_copies_from_groups(files_groups):

        show_list_files(copies, TEXTS['identical_files'])

        if not delete:
            continue

        # wait user input
        nums = get_nums_for_delete(copies)

        # if users choice not delete files
        if 0 in nums:
            continue

        files_to_delete = [copies[num - 1] for num in nums]

        # show files to delete
        show_list_files(files_to_delete, TEXTS['delete_list'])

        if click.confirm(TEXTS['confirm']):
            delete_files(files_to_delete)
            click.echo(TEXTS['delete_success'])
        else:
            click.echo(TEXTS['delete_aborted'])

        click.echo('=' * 20)


if __name__ == '__main__':
    find_copies()
