# tests/test_verify.py

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
import urllib.error
from relm.verify import verify_project_release
from relm.core import Project

class TestVerify(unittest.TestCase):
    def setUp(self):
        self.project = Project(
            name="test-project",
            version="6.0.0",
            path=Path("/tmp/test_project"),
            description="Test project"
        )

    @patch("relm.verify.git_tag_exists")
    @patch("urllib.request.urlopen")
    def test_verify_success(self, mock_urlopen, mock_tag_exists):
        mock_tag_exists.return_value = True
        
        # Mock PyPI response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "releases": {self.project.version: [], "0.9.0": []},
            "info": {"version": self.project.version}
        }).encode()
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        success, message = verify_project_release(self.project)
        self.assertTrue(success)
        self.assertIn("is verified on PyPI", message)

    @patch("relm.verify.git_tag_exists")
    def test_verify_missing_tag(self, mock_tag_exists):
        mock_tag_exists.return_value = False
        
        success, message = verify_project_release(self.project)
        self.assertFalse(success)
        self.assertIn(f"Local git tag 'v{self.project.version}' does not exist", message)

    @patch("relm.verify.git_tag_exists")
    @patch("urllib.request.urlopen")
    def test_verify_version_not_found(self, mock_urlopen, mock_tag_exists):
        mock_tag_exists.return_value = True
        
        # Mock PyPI response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "releases": {"0.9.0": []},
            "info": {"version": "0.9.0"}
        }).encode()
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        success, message = verify_project_release(self.project)
        self.assertFalse(success)
        self.assertIn("not found on PyPI", message)
        self.assertIn("Latest is 0.9.0", message)

    @patch("relm.verify.git_tag_exists")
    @patch("urllib.request.urlopen")
    def test_verify_404_error(self, mock_urlopen, mock_tag_exists):
        mock_tag_exists.return_value = True
        
        # Mock PyPI 404
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "url", 404, "Not Found", {}, None
        )
        
        success, message = verify_project_release(self.project)
        self.assertFalse(success)
        self.assertIn("Failed to query PyPI", message)

    @patch("relm.verify.git_tag_exists")
    @patch("urllib.request.urlopen")
    def test_verify_json_error(self, mock_urlopen, mock_tag_exists):
        mock_tag_exists.return_value = True
        
        mock_response = MagicMock()
        mock_response.read.return_value = b"Not JSON"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        success, message = verify_project_release(self.project)
        self.assertFalse(success)
        self.assertIn("Failed to parse PyPI response", message)

if __name__ == "__main__":
    unittest.main()
