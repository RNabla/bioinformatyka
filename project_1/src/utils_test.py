import unittest
from utils import assert_required_keys


class UtilsTest(unittest.TestCase):
    def test_assert_required_keys(self):
        config = {'same': 5}
        required_keys = ['same', 'diff']
        with self.assertRaises(KeyError):
            assert_required_keys(config, required_keys)
