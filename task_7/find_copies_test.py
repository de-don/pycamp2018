from unittest import TestCase
from pathlib import Path
from .find_copies import *


class FuncsTest(TestCase):
    def test_sha1_copies(self):
        file_1 = Path("task_7/test_files/copies/other/file_1.txt")
        file_2 = Path("task_7/test_files/copies/other/file_2.txt")

        self.assertEqual(get_file_sha1(file_1), get_file_sha1(file_2))

    def test_sha1_different(self):
        file_1 = Path("task_7/test_files/copies/file_3.txt")
        file_2 = Path("task_7/test_files/copies/file_4.txt")

        self.assertNotEqual(get_file_sha1(file_1), get_file_sha1(file_2))

    def test_empty_files_1(self):
        items = Path("task_7/test_files").iterdir()
        files = [item for item in items if not item.is_dir()]
        self.assertEqual(len(files), 2)

        count = len(list(non_empty_files(files)))
        self.assertEqual(count, 0)

    def test_empty_files_2(self):
        items = Path("task_7/test_files/libs").iterdir()
        files = [item for item in items if not item.is_dir()]
        self.assertEqual(len(files), 3)

        count = len(list(non_empty_files(files)))
        self.assertEqual(count, 3)

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