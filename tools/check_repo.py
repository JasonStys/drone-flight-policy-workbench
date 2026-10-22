"""Jason Stys: public source, policy builtin, immutable CI and payload hygiene. Lines: docs/SOURCE_MAP.md."""

import gzip
import re

from docs_index import ROOT, files


def main():
    """Check complete source headers, narrow secret signatures, binary-free source and fixed CI refs."""
    for path in files():
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8")
        if path.suffix in {".py", ".ts", ".mjs", ".rego", ".sql"}:
            assert "Jason Stys:" in content[:600] and "docs/SOURCE_MAP.md" in content[:600], (
                relative
            )
        assert not re.search(r"(?:ghp_|github_pat_)[A-Za-z0-9_]{30,}", content), relative
        assert ("-----BEGIN " + "PRIVATE KEY-----") not in content, relative
        assert path.suffix not in {".exe", ".db", ".sqlite3"}, relative
        if relative.startswith(".github/workflows/"):
            for ref in re.findall(r"uses:\s*([^\s]+)", content):
                assert re.search(r"@[0-9a-f]{40}$", ref), ref
            assert "upload-artifact" not in content and "actions/cache" not in content
        if path.suffix == ".rego":
            assert not any(
                builtin in content for builtin in ("http.send", "net.lookup_ip_addr", "opa.runtime")
            ), relative
    for suffix, budget in [("js", 40000), ("css", 12000)]:
        size = sum(
            len(gzip.compress(p.read_bytes())) for p in (ROOT / "dist/assets").glob(f"*.{suffix}")
        )
        assert 0 < size <= budget, (suffix, size, budget)
        print(f"Built {suffix}: {size} gzip bytes / {budget} budget")
    print("Source/policy/immutable workflow hygiene passed")


if __name__ == "__main__":
    main()
