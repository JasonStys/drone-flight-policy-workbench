"""Jason Stys: original synthetic organizational policy and fictional operation cases. Lines: docs/SOURCE_MAP.md."""

import copy

from workbench.models import Operation, Policy

FAA = "https://www.faa.gov/uas/getting_started/laanc"
REMOTE = "https://www.faa.gov/uas/getting_started/remote_id"
PRIVACY = (
    "https://www.ntia.gov/other-publication/2016/multistakeholder-process-unmanned-aircraft-systems"
)
ORG = "https://github.com/JasonStys/drone-flight-policy-workbench/blob/main/docs/EXAMPLE_POLICY.md"


def example_policy():
    """A configurable organizational subset, not encoded law or an FAA approval workflow."""
    definitions = [
        (
            "credential",
            "Credential evidence current",
            "credential_current",
            "equals",
            True,
            None,
            FAA,
        ),
        (
            "registration",
            "Registration evidence current",
            "registration_current",
            "equals",
            True,
            None,
            REMOTE,
        ),
        (
            "remote-id",
            "Remote ID applicability reviewed",
            "remote_id_reviewed",
            "equals",
            True,
            None,
            REMOTE,
        ),
        (
            "restrictions",
            "Official restrictions checked",
            "restrictions_checked",
            "equals",
            True,
            None,
            FAA,
        ),
        ("vlos", "Visual observation plan recorded", "vlos_plan", "equals", True, None, ORG),
        (
            "airspace",
            "Authorization evidence recorded",
            "airspace_authorized",
            "equals",
            True,
            "controlled_airspace",
            FAA,
        ),
        (
            "privacy",
            "Privacy and minimization plan",
            "privacy_plan",
            "equals",
            True,
            "camera_requested",
            PRIVACY,
        ),
        (
            "site",
            "Sensitive site permission",
            "sensitive_site_permission",
            "equals",
            True,
            "sensitive_site",
            ORG,
        ),
        (
            "emergency",
            "Emergency coordination recorded",
            "emergency_coordination",
            "equals",
            True,
            "emergency_operation",
            ORG,
        ),
        (
            "altitude",
            "Organizational altitude cap in metres",
            "altitude_agl_m",
            "max",
            100.0,
            None,
            ORG,
        ),
        ("wind", "Organizational wind cap in metres per second", "wind_mps", "max", 8.0, None, ORG),
        (
            "retention",
            "Organizational retention cap in days",
            "retention_days",
            "max",
            7.0,
            "camera_requested",
            PRIVACY,
        ),
    ]
    return Policy.model_validate(
        {
            "name": "Synthetic organization baseline",
            "valid_from_s": 900,
            "valid_until_s": 2000,
            "rules": [
                {
                    "id": identifier,
                    "title": title,
                    "fact": fact,
                    "comparator": comparator,
                    "expected": expected,
                    "when_fact": condition,
                    "source_url": url,
                    "reference": "Research 2026-10-22 - example organization check",
                }
                for identifier, title, fact, comparator, expected, condition, url in definitions
            ],
        }
    )


def example_operation():
    """All sample claims are fictional and attested only within the synthetic exercise."""
    values = {
        "credential_current": True,
        "registration_current": True,
        "remote_id_reviewed": True,
        "airspace_authorized": True,
        "restrictions_checked": True,
        "vlos_plan": True,
        "privacy_plan": True,
        "emergency_coordination": True,
        "sensitive_site_permission": True,
        "controlled_airspace": True,
        "camera_requested": True,
        "sensitive_site": False,
        "emergency_operation": False,
        "altitude_agl_m": 80.0,
        "wind_mps": 5.0,
        "retention_days": 3.0,
    }
    return Operation.model_validate(
        {
            "name": "Synthetic infrastructure inspection",
            "jurisdiction": "US",
            "framework": "PART_107",
            "as_of_s": 1000,
            "evidence": [
                {
                    "id": f"claim-{n}",
                    "fact": fact,
                    "value": value,
                    "source_ref": f"Synthetic record {n}",
                    "observed_s": 990,
                    "expires_s": 1100,
                    "attested": True,
                }
                for n, (fact, value) in enumerate(values.items())
            ],
        }
    )


def examples():
    """Return satisfied/unknown/blocked examples plus expired evidence, without operational data."""
    baseline = example_operation().model_dump()
    missing = copy.deepcopy(baseline)
    missing["name"] = "Flood survey missing authorization evidence"
    missing["evidence"] = [e for e in missing["evidence"] if e["fact"] != "airspace_authorized"]
    privacy = copy.deepcopy(baseline)
    privacy["name"] = "Sensitive inspection privacy hold"
    for record in privacy["evidence"]:
        if record["fact"] == "retention_days":
            record["value"] = 30.0
        if record["fact"] == "sensitive_site":
            record["value"] = True
    expired = copy.deepcopy(baseline)
    expired["name"] = "Emergency exercise expired registration record"
    for record in expired["evidence"]:
        if record["fact"] == "registration_current":
            record["expires_s"] = 999
        if record["fact"] == "emergency_operation":
            record["value"] = True
    return {
        "inspection": baseline,
        "missing-approval": missing,
        "privacy-hold": privacy,
        "expired-record": expired,
    }
