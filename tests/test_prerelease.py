import pytest
from relm.versioning import bump_version_string

@pytest.mark.parametrize("current, part, expected", [
    ("1.0.0", "alpha", "1.0.1-alpha.1"),
    ("1.0.1-alpha.1", "alpha", "1.0.1-alpha.2"),
    ("1.0.1-alpha.2", "alpha", "1.0.1-alpha.3"),
    ("1.0.1-alpha.1", "beta", "1.0.1-beta.1"),
    ("1.0.1-beta.1", "beta", "1.0.1-beta.2"),
    ("1.0.1-beta.2", "rc", "1.0.1-rc.1"),
    ("1.0.1-rc.1", "rc", "1.0.1-rc.2"),
    ("1.0.1-rc.2", "release", "1.0.1"),
    ("1.0.1", "patch", "1.0.2"),
    ("1.0.1-rc.1", "patch", "1.0.2"), # Moving from a pre-release to next patch (skipping final release of 1.0.1)
])
def test_bump_prerelease(current, part, expected):
    assert bump_version_string(current, part) == expected
