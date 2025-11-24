import unittest
from relm.versioning import bump_version_string

class TestVersioning(unittest.TestCase):
    def test_bump_patch(self):
        self.assertEqual(bump_version_string("1.0.0", "patch"), "1.0.1")
        self.assertEqual(bump_version_string("0.0.9", "patch"), "0.0.10")

    def test_bump_minor(self):
        self.assertEqual(bump_version_string("1.0.5", "minor"), "1.1.0")
        self.assertEqual(bump_version_string("0.1.0", "minor"), "0.2.0")

    def test_bump_major(self):
        self.assertEqual(bump_version_string("1.5.9", "major"), "2.0.0")
        self.assertEqual(bump_version_string("0.0.1", "major"), "1.0.0")

    def test_incomplete_version(self):
        # "0.1" treated as "0.1.0"
        self.assertEqual(bump_version_string("0.1", "patch"), "0.1.1")

if __name__ == "__main__":
    unittest.main()
