"""Check statement files against statements/MANIFEST.sha256.

    python3 tools/verify_statements.py statements/stmt-001.txt [more files...]

Each check takes about five seconds on purpose: it models the call to the
core-banking statement archive, which answers that slowly. Tests pass
delay=0 to skip the wait.

Exit code 0 when every file matches, 1 otherwise.
"""

import hashlib
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "statements" / "MANIFEST.sha256"
CORE_BANKING_DELAY_SECONDS = 5.0


def load_manifest(path=MANIFEST):
    """File name to SHA-256, from lines of the form '<sha256>  <file name>'."""
    entries = {}
    for line in path.read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        entries[name] = digest
    return entries


def verify_file(path, manifest, delay=CORE_BANKING_DELAY_SECONDS):
    """'ok', 'MISMATCH' or 'NOT IN MANIFEST' for one statement file."""
    time.sleep(delay)
    expected = manifest.get(path.name)
    if expected is None:
        return "NOT IN MANIFEST"
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    return "ok" if actual == expected else "MISMATCH"


def main(argv=None):
    paths = [Path(p) for p in (sys.argv[1:] if argv is None else argv)]
    if not paths:
        sys.exit(__doc__)
    manifest = load_manifest()
    failures = 0
    for path in paths:
        result = verify_file(path, manifest)
        failures += result != "ok"
        print(f"{path.name}: {result}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
