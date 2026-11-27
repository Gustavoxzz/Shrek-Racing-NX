import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("compare_packets", Path(__file__).parents[1] / "tools" / "compare_packets.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ComparePacketsTest(unittest.TestCase):
    def test_equal_with_distinct_alignment(self):
        result = module.compare(b"abc", b"abc", 16, 19)
        self.assertTrue(result["equal"])
        self.assertEqual(result["b"]["offset_mod_16"], 3)
        self.assertIsNone(result["first_difference"])

    def test_first_difference_and_length(self):
        self.assertEqual(module.compare(b"abc", b"axc", 0, 0)["first_difference"], 1)
        self.assertEqual(module.compare(b"a", b"ab", 0, 0)["first_difference"], 1)

    def test_rejects_invalid_input(self):
        with self.assertRaises(ValueError):
            module.compare(b"", b"", -1, 0)
        with self.assertRaises(ValueError):
            module.compare(b"x" * (module.MAX_PACKET + 1), b"", 0, 0)


if __name__ == "__main__":
    unittest.main()
