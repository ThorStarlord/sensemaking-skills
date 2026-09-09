"""Sensemaking Skills package."""

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover - Python 3.7 compatibility
    from importlib_metadata import PackageNotFoundError, version  # type: ignore


def _distribution_version() -> str:
    """Return installed release metadata without creating a second authority."""
    try:
        return version("sensemaking-skills")
    except PackageNotFoundError:  # source checkout without installed metadata
        return "0+unknown"


__version__ = _distribution_version()


__all__ = ["__version__"]
