import unittest
from pathlib import Path
from repo_manager.core import find_projects

class TestCore(unittest.TestCase):
    def test_find_projects(self):
        # We assume we are running in the 'tools' directory which has projects
        root = Path(".")
        projects = find_projects(root)
        
        # Should find at least repo_manager itself
        names = [p.name for p in projects]
        
        self.assertIn("repo_manager", names)
        self.assertTrue(len(projects) > 1)

if __name__ == "__main__":
    unittest.main()
