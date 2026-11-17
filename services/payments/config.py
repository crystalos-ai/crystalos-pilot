"""Database settings for the payments service.

Settings live in `db.<name>.conf` files next to this module, one KEY=value per
line. A config never holds a password: it names the environment variable that
does (DATABASE_PASSWORD_ENV).

Only the local SQLite database is opened from this repository. Production runs
on PostgreSQL through the platform team's deployment, which is not part of this
repository.
"""

from pathlib import Path

HERE = Path(__file__).parent
REPO_ROOT = HERE.parent.parent
SQLITE_PREFIX = "sqlite:///"


def load_config(name="local"):
    settings = {}
    for line in (HERE / f"db.{name}.conf").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        settings[key.strip()] = value.strip()
    return settings


def sqlite_path(settings):
    """The local SQLite file a config points at. Refuses any other database."""
    url = settings["DATABASE_URL"]
    if not url.startswith(SQLITE_PREFIX):
        raise ValueError(f"not a local SQLite database: {url}")
    return REPO_ROOT / url[len(SQLITE_PREFIX):]
