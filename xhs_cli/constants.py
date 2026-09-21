"""Constants for XHS API client."""

API_HOSTS = {
    "rednote": "https://webapi.rednote.com",
    "xiaohongshu": "https://edith.xiaohongshu.com",
}
HOME_URLS = {
    "rednote": "https://www.rednote.com",
    "xiaohongshu": "https://www.xiaohongshu.com",
}
CREATOR_HOSTS = {
    "rednote": "https://webapi.rednote.com",
    "xiaohongshu": "https://creator.xiaohongshu.com",
}
UPLOAD_HOSTS = {
    "rednote": "https://webapi.rednote.com",
    "xiaohongshu": "https://ros-upload.xiaohongshu.com",
}

# Legacy aliases retained for signing/import compatibility.
EDITH_HOST = API_HOSTS["xiaohongshu"]
CREATOR_HOST = CREATOR_HOSTS["xiaohongshu"]
HOME_URL = HOME_URLS["xiaohongshu"]
UPLOAD_HOST = UPLOAD_HOSTS["xiaohongshu"]

CHROME_VERSION = "145"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    f"Chrome/{CHROME_VERSION}.0.0.0 Safari/537.36"
)

SDK_VERSION = "4.2.6"
APP_ID = "xhs-pc-web"
PLATFORM = "macOS"

# Config directory
CONFIG_DIR_NAME = ".rednote-cli"
DEFAULT_COOKIE_DOMAIN = "rednote"
COOKIE_DOMAINS = {
    "rednote": "rednote.com",
    "xiaohongshu": "xiaohongshu.com",
}


def profile_hosts(cookie_domain: str) -> dict[str, str]:
    """Return API, web, creator, and upload hosts for a cookie profile."""
    if cookie_domain not in API_HOSTS:
        choices = ", ".join(API_HOSTS)
        raise ValueError(f"Unknown cookie domain profile: {cookie_domain!r}. Choose from: {choices}")
    return {
        "api": API_HOSTS[cookie_domain],
        "home": HOME_URLS[cookie_domain],
        "creator": CREATOR_HOSTS[cookie_domain],
        "upload": UPLOAD_HOSTS[cookie_domain],
    }
COOKIE_FILE_TEMPLATE = "cookies.{profile}.json"
LEGACY_COOKIE_FILE = "cookies.json"
TOKEN_CACHE_FILE = "token_cache.json"
INDEX_CACHE_FILE = "index_cache.json"
