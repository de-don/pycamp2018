from unittest import TestCase
from unittest.mock import Mock, patch
from pathlib import Path
from .find_copies import (
    find_copies,
    get_file_sha1,
    process_str_of_nums,
    sha1_copies,
    recursion_finder,
    TEXTS,
    delete_files)
from click.testing import CliRunner


class FuncsTest(TestCase):
    def test_sha1_equal(self):
        file_1 = Path("task_7/test_files/copies/other/file_1.txt")
        file_2 = Path("task_7/test_files/copies/other/file_2.txt")

        self.assertEqual(get_file_sha1(file_1), get_file_sha1(file_2))

    def test_sha1_different(self):
        file_1 = Path("task_7/test_files/copies/file_3.txt")
        file_2 = Path("task_7/test_files/copies/file_4.txt")

        self.assertNotEqual(get_file_sha1(file_1), get_file_sha1(file_2))

    def test_recursion_finder(self):
        path = Path("task_7/test_files/copies")
        files = list(recursion_finder(path))
        self.assertEqual(len(files), 5)

    def test_process_str_of_nums(self):
        nums = " ".join(map(str, range(5)))
        result = process_str_of_nums(nums)
        self.assertEqual(list(range(5)), list(result))

    def test_process_str_of_nums_range(self):
        nums = " ".join(map(str, range(5)))
        result = process_str_of_nums(nums, range_num=(0, 4))
        self.assertEqual(list(range(5)), list(result))

    def test_process_str_of_nums_range_error(self):
        nums = " ".join(map(str, range(5)))
        with self.assertRaises(IndexError):
            next(process_str_of_nums(nums, range_num=(1, 2)))

    def test_sha1_copies(self):
        file_1 = Path("task_7/test_files/copies/file_3.txt")
        file_2 = Path("task_7/test_files/copies/file_4.txt")
        file_3 = Path("task_7/test_files/copies/file_5.txt")

        gen = sha1_copies([file_1, file_2, file_3])
        items = next(gen)

        self.assertEqual(len(items), 2)
        self.assertListEqual(items, [file_1, file_3])

    def test_runner(self):
        runner = CliRunner()
        result = runner.invoke(find_copies, ['task_7/test_files'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            TEXTS['identical_files'] + '\n'
            '    1) task_7/test_files/libs/super_lib.txt\n'
            '    2) task_7/test_files/libs/super_lib_copy.txt\n' +
            TEXTS['identical_files'] + '\n'
            '    1) task_7/test_files/copies/file_4.txt\n'
            '    2) task_7/test_files/copies/other/file_1.txt\n'
            '    3) task_7/test_files/copies/other/file_2.txt\n' +
            TEXTS['identical_files'] + '\n'
            '    1) task_7/test_files/copies/file_5.txt\n'
            '    2) task_7/test_files/copies/file_3.txt\n'
        )

    def test_runner_deleter(self):
        runner = CliRunner()
        result = runner.invoke(
            find_copies,
            ['task_7/test_files/copies/other/', '-d'],
            input='1\nN',
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.output,
            TEXTS['identical_files'] + '\n'
            '    1) task_7/test_files/copies/other/file_1.txt\n'
            '    2) task_7/test_files/copies/other/file_2.txt\n' +
            TEXTS['delete'] + ' [0]: 1\n' +
            TEXTS['delete_list'] + '\n'
            '    1) task_7/test_files/copies/other/file_1.txt\n' +
            TEXTS['confirm'] + ' [y/N]: N\n' +
            TEXTS['delete_aborted'] + '\n'
            '====================\n'
        )

    def test_delete_files_1(self):
        files = [Mock(name=f'file_{i}') for i in range(5)]
        delete_files(files)
        self.assertTrue(all(file._accessor.unlink.called for file in files))

    def test_delete_files_2(self):
        files = range(5)

        with patch('pathlib.Path.unlink') as mock_unlink:
            delete_files(files)
            self.assertEqual(mock_unlink.call_count, 5)