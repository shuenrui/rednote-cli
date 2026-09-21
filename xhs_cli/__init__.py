"""rednote-cli: Xiaohongshu CLI using RedNote browser cookies."""

try:
    from importlib.metadata import version

    __version__ = version("rednote-cli")
except Exception:
    __version__ = "0.0.0"
