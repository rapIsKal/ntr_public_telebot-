import unittest

from utils.name_matcher import revert_dicts


class TestUtils(unittest.TestCase):
    def test_reverse_dict(self):
        inp = {"a": ["b", "c", "d"], "e": ["f"]}
        exp ={"b": "a", "c": "a", "d": "a", "f": "e"}
        self.assertDictEqual(revert_dicts(inp), exp)