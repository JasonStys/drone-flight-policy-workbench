"""Jason Stys: release version, source cleanliness and archive acceptance contracts. Lines: docs/SOURCE_MAP.md."""

import hashlib
import json
import os
import stat
import subprocess
import sys

import pytest

from tools import package_app


def test_collected_vendor_bytes_and_mode_are_restored_without_reblessing_digest(tmp_path):
    """A changed collected helper is replaced by the exact independently pinned original, never a new trusted hash."""
    source = tmp_path / "opa_darwin_arm64_static"
    source.write_bytes(b"controlled-original-vendor-fixture")
    source.chmod(0o751)
    expected = hashlib.sha256(source.read_bytes()).hexdigest()
    bundle = tmp_path / "bundle"
    target = bundle / "_internal/vendor/opa" / source.name
    target.parent.mkdir(parents=True)
    target.write_bytes(b"changed-by-collection")
    result = package_app.restore_vendor_opa(bundle, source, expected)
    assert result == {
        "official_sha256": expected,
        "collected_sha256": hashlib.sha256(b"changed-by-collection").hexdigest(),
        "packaged_sha256": expected,
    }
    assert target.read_bytes() == source.read_bytes()
    assert os.name == "nt" or stat.S_IMODE(target.stat().st_mode) == 0o751
    source.write_bytes(b"unexpected-source-change")
    before = target.read_bytes()
    with pytest.raises(ValueError, match="source OPA changed"):
        package_app.restore_vendor_opa(bundle, source, expected)
    assert target.read_bytes() == before


def test_missing_noncanonical_or_unowned_vendor_paths_cannot_be_created(tmp_path):
    """Restore never creates an absent destination or accepts relative/aliased build or source paths."""
    source = tmp_path / "opa_darwin_arm64_static"
    source.write_bytes(b"fixed-vendor-fixture")
    expected = hashlib.sha256(source.read_bytes()).hexdigest()
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    with pytest.raises(ValueError, match="missing or not owned"):
        package_app.restore_vendor_opa(bundle, source, expected)
    assert list(bundle.iterdir()) == []
    with pytest.raises(ValueError, match="Absolute"):
        package_app.restore_vendor_opa(bundle, source.relative_to(tmp_path), expected)
    with pytest.raises(ValueError, match="canonical"):
        package_app.restore_vendor_opa(bundle / ".." / "bundle", source, expected)


@pytest.mark.parametrize(
    "version,level,allowed",
    [
        ((), "final", False),
        ((3, 14, 6), "final", False),
        ((3, 12, 16), "final", False),
        ((3, 14, 10), "candidate", False),
        ((3, 14, 10), "final", True),
        ((3, 14, 11), "final", True),
        ((3, 15, 0), "final", False),
    ],
)
def test_freeze_refuses_old_cached_or_prerelease_runtime(version, level, allowed):
    """A clean source checkout cannot hide an outdated or experimental embedded Python runtime."""
    assert package_app.build_python_supported(version, level) is allowed


def test_all_product_version_surfaces_agree():
    """The packaged product and runtime version agree independently of domain schema versions."""
    from workbench import __version__

    assert package_app.configuration() == __version__ == "0.2.0"
    assert package_app.PRODUCT == "drone-flight-policy-workbench"


@pytest.mark.parametrize(
    "surface", ["project", "package", "lock", "lock-root", "runtime", "product"]
)
def test_mismatched_version_or_identity_cannot_build(tmp_path, surface):
    """Independent tiny real files expose any one stale or wrong product/version declaration."""
    root = package_app.ROOT
    for path in ("pyproject.toml", "package.json", "package-lock.json", "workbench/__init__.py"):
        output = tmp_path / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes((root / path).read_bytes())
    selected = {
        "project": "pyproject.toml",
        "package": "package.json",
        "lock": "package-lock.json",
        "lock-root": "package-lock.json",
        "runtime": "workbench/__init__.py",
        "product": "package.json",
    }[surface]
    path = tmp_path / selected
    if surface in {"project", "runtime"}:
        path.write_text(path.read_text().replace("0.2.0", "0.1.0"))
    else:
        value = json.loads(path.read_text())
        if surface == "lock-root":
            value["packages"][""]["version"] = "0.1.0"
        elif surface == "product":
            value["name"] = "other-project"
        else:
            value["version"] = "0.1.0"
        path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="mismatch"):
        package_app.configuration(tmp_path)


@pytest.mark.parametrize(
    "dirty,ci,override,sha,allowed",
    [
        (False, False, False, None, True),
        (True, False, False, None, False),
        (True, False, True, None, True),
        (True, True, True, "a" * 40, False),
        (False, True, True, "a" * 40, False),
        (False, True, False, "b" * 40, False),
        (False, True, False, "a" * 40, True),
    ],
)
def test_source_cleanliness_is_not_a_release_flag_waiver(
    monkeypatch, dirty, ci, override, sha, allowed
):
    """Local uncommitted candidate is explicit; CI cannot use the override or a different checkout."""

    def output(command, **_kwargs):
        return (
            "a" * 40 + "\n"
            if command[-2:] == ["rev-parse", "HEAD"]
            else " M source.py\n"
            if dirty
            else ""
        )

    monkeypatch.setattr(package_app.subprocess, "check_output", output)
    monkeypatch.setenv("GITHUB_ACTIONS", "true" if ci else "false")
    if sha:
        monkeypatch.setenv("GITHUB_SHA", sha)
    if not allowed:
        with pytest.raises(ValueError):
            package_app.source_metadata("0.2.0", allow_dirty=override)
    else:
        value = package_app.source_metadata("0.2.0", allow_dirty=override)
        assert value["source_commit"] == "a" * 40 and value["source_dirty"] is dirty


def test_archive_rejection_remains_active_with_optimized_python():
    """An actual optimized child still rejects path escape before creating any output."""
    result = subprocess.run(
        [
            sys.executable,
            "-O",
            "-c",
            "from tools.portable_archive import safe_name; safe_name('../escape', 'ExampleApp')",
        ],
        cwd=package_app.ROOT,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode != 0 and "Unsafe archive member path" in result.stderr
