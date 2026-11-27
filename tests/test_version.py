import re

from triggerdev import __version__


def test_version_is_string() -> None:
    assert isinstance(__version__, str)


def test_version_is_semver() -> None:
    assert re.match(r"^\d+\.\d+\.\d+$", __version__)
