"""Jason Stys: verified native OPA format, strict-check and coverage gates. Lines: docs/SOURCE_MAP.md."""

import json
import subprocess

from tools.fetch_opa import ROOT, binary


def main():
    """Use the same verified vendor release as production; do not substitute a Python-only pass."""
    path = str(binary())
    for args in [
        ["fmt", "--fail", "policies"],
        ["check", "--strict", "policies"],
        ["test", "--coverage", "--threshold=90", "--verbose", "policies"],
    ]:
        completed = subprocess.run(
            [path, *args], cwd=ROOT, check=True, timeout=60, capture_output=True, text=True
        )
        if args[0] == "test":
            report = json.loads(completed.stdout)
            (ROOT / ".runtime/opa/coverage.json").write_text(completed.stdout, encoding="utf-8")
            print(
                json.dumps(
                    {
                        "overall_coverage": report["coverage"],
                        "files": {name: item["coverage"] for name, item in report["files"].items()},
                        "threshold": 90,
                    }
                )
            )
        else:
            print(f"OPA {args[0]}: passed")


if __name__ == "__main__":
    main()
