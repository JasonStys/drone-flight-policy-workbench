"""Jason Stys: explicit official OPA installer with release-pinned SHA256s. Lines: docs/SOURCE_MAP.md.

Only this setup command downloads; the running application never downloads or calls providers.
"""

import hashlib
import platform
import stat
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v1.21.3"
RELEASES = {
    ("win32", "amd64"): (
        "opa_windows_amd64.exe",
        "c8f08ee67544be8ca47b063f6656091c1dcb4aba6434c2cd4c5b498b0dcfa115",
    ),
    ("linux", "x86_64"): (
        "opa_linux_amd64_static",
        "add7c9dcf56e1ce1538426a6ee595ea1cc7ee830bbedd4c23219825b02b19a79",
    ),
    ("linux", "aarch64"): (
        "opa_linux_arm64_static",
        "45c8734a41436bf21d82453c2aa7b0ad47c150e8237310b8665e8b5a01305fc0",
    ),
    ("darwin", "x86_64"): (
        "opa_darwin_amd64",
        "3ef285e7e2cf57e6cb05142c33002e07d6791580a4ac14bac0a4e0880dfe073d",
    ),
    ("darwin", "arm64"): (
        "opa_darwin_arm64_static",
        "ee96aae344f45dd63044be2bedcba6391ca78402760b204a747331f421db74fe",
    ),
}


def binary():
    """Resolve only our fixed local binary and verify release identity before execution."""
    name, checksum = RELEASES[(sys.platform, platform.machine().lower())]
    path = ROOT / ".runtime/opa" / name
    with path.open("rb") as source:
        actual = hashlib.file_digest(source, "sha256").hexdigest()
    if actual != checksum:
        raise ValueError("OPA checksum mismatch; refusing to execute")
    return path


def main():
    """Install from fixed vendor HTTPS release, limit download size, then verify checksum."""
    name, _ = RELEASES[(sys.platform, platform.machine().lower())]
    path = ROOT / ".runtime/opa" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        with (
            urllib.request.urlopen(
                f"https://github.com/open-policy-agent/opa/releases/download/{VERSION}/{name}",
                timeout=60,
            ) as response,
            path.open("wb") as output,
        ):  # noqa: S310 - fixed official vendor HTTPS release
            total = 0
            while chunk := response.read(1024 * 1024):
                total += len(chunk)
                if total > 256 * 1024 * 1024:
                    raise ValueError("OPA download exceeds size cap")
                output.write(chunk)
    path = binary()
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    print(f"Verified official OPA {VERSION}: {path.name}")


if __name__ == "__main__":
    main()
