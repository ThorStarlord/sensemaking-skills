"""Sensemaking Skills: agent-native repository sensemaking and Campaign control."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("sensemaking-skills")
except PackageNotFoundError:  # Source tree used without an installed distribution.
    __version__ = "0+unknown"

__author__ = "Dimmi Andreus"
__email__ = "dimmi.andreus1@gmail.com"

__all__ = ["__version__"]
