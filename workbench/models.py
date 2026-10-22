"""Jason Stys: finite closed contracts, SI units and contradiction rejection. Lines: docs/SOURCE_MAP.md."""

import math
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictStr,
    model_validator,
)

Label = Annotated[str, Field(strict=True, pattern=r"^[A-Za-z0-9][A-Za-z0-9 _.-]{0,79}$")]
Key = Literal[
    "credential_current",
    "registration_current",
    "remote_id_reviewed",
    "airspace_authorized",
    "restrictions_checked",
    "vlos_plan",
    "privacy_plan",
    "emergency_coordination",
    "sensitive_site_permission",
    "controlled_airspace",
    "camera_requested",
    "sensitive_site",
    "emergency_operation",
    "altitude_agl_m",
    "wind_mps",
    "retention_days",
]
NUMERIC = {"altitude_agl_m", "wind_mps", "retention_days"}
Value = StrictBool | StrictFloat | StrictStr | None
Clock = Annotated[int, Field(strict=True, ge=0, le=4_000_000_000)]


def valid_value(key, value):
    """Prevent booleans-as-numbers, string coercion, unsupported units and nonfinite measurements."""
    if value is None:
        return
    if key in NUMERIC:
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 100_000:
            raise ValueError("Numeric facts require finite nonnegative SI values within bounds")
    elif type(value) is not bool:
        raise ValueError("Boolean facts require true, false or null")


class Contract(BaseModel):
    """Reject extra fields and silent type conversions at every nested boundary."""

    model_config = ConfigDict(extra="forbid", strict=True)


class Evidence(Contract):
    """One human-supplied claim; attestation is not independent agency verification."""

    id: Label
    fact: Key
    value: Value
    source_ref: Label
    observed_s: Clock
    expires_s: Clock
    attested: bool = False

    @model_validator(mode="after")
    def coherent(self):
        """Validate field type and time interval without inventing absent facts."""
        valid_value(self.fact, self.value)
        if self.expires_s < self.observed_s:
            raise ValueError("Evidence expires before observation")
        return self


class Rule(Contract):
    """One bounded data-only rule; users cannot submit executable Rego or URLs to fetch."""

    id: Label
    title: Label
    fact: Key
    comparator: Literal["equals", "max", "min"]
    expected: StrictBool | StrictFloat
    max_age_s: Annotated[int, Field(strict=True, ge=1, le=86400)] = 300
    when_fact: Key | None = None
    when_value: bool = True
    source_url: Annotated[
        str,
        Field(
            strict=True, max_length=512, pattern=r"^https://[A-Za-z0-9.-]+/[A-Za-z0-9_./?=%#&+-]*$"
        ),
    ]
    reference: Label

    @model_validator(mode="after")
    def typed(self):
        """Keep comparisons dimensionally consistent and conditions strictly boolean."""
        valid_value(self.fact, self.expected)
        if self.fact not in NUMERIC and self.comparator != "equals":
            raise ValueError("Boolean facts only support equals")
        if self.when_fact in NUMERIC:
            raise ValueError("Conditions must reference boolean facts")
        if self.when_fact == self.fact:
            raise ValueError("A rule cannot conditionally waive its own fact")
        return self


class Policy(Contract):
    """Immutable version content with explicit context and validity window."""

    name: Label
    jurisdiction: Literal["US"] = "US"
    framework: Literal["PART_107"] = "PART_107"
    valid_from_s: Clock
    valid_until_s: Clock
    rules: Annotated[list[Rule], Field(min_length=1, max_length=40)]

    @model_validator(mode="after")
    def consistent(self):
        """Reject duplicate IDs and contradictory simultaneously applicable rule bounds."""
        if self.valid_from_s >= self.valid_until_s or len({r.id for r in self.rules}) != len(
            self.rules
        ):
            raise ValueError("Invalid policy window or duplicate rule IDs")
        for i, a in enumerate(self.rules):
            for b in self.rules[i + 1 :]:
                if a.fact != b.fact:
                    continue
                if (
                    a.when_fact == b.when_fact
                    and a.when_fact is not None
                    and a.when_value != b.when_value
                ):
                    continue
                if a.comparator == b.comparator == "equals" and a.expected != b.expected:
                    raise ValueError("Contradictory equality rules")
                if a.fact in NUMERIC:
                    lo = (
                        max(float(r.expected) for r in (a, b) if r.comparator in ("min", "equals"))
                        if any(r.comparator in ("min", "equals") for r in (a, b))
                        else 0
                    )
                    hi = (
                        min(float(r.expected) for r in (a, b) if r.comparator in ("max", "equals"))
                        if any(r.comparator in ("max", "equals") for r in (a, b))
                        else 100_000
                    )
                    if lo > hi:
                        raise ValueError("Contradictory numeric rules")
        return self


class Operation(Contract):
    """A synthetic proposed operation; no real pilot IDs, geolocation or aircraft control."""

    name: Label
    jurisdiction: Literal["US", "OTHER", "UNKNOWN"] = "UNKNOWN"
    framework: Literal["PART_107", "OTHER", "UNKNOWN"] = "UNKNOWN"
    as_of_s: Clock
    evidence: Annotated[list[Evidence], Field(max_length=128)]

    @model_validator(mode="after")
    def unique(self):
        """Avoid ambiguous evidence references; contradictory facts are kept for explicit review."""
        if len({e.id for e in self.evidence}) != len(self.evidence):
            raise ValueError("Evidence IDs must be unique")
        return self


class Login(Contract):
    """Bound credentials before Argon2; never reflect submitted values in errors."""

    username: Annotated[str, Field(strict=True, min_length=3, max_length=40)]
    password: Annotated[str, Field(strict=True, min_length=1, max_length=128)]


class Evaluate(Contract):
    """Expected active version prevents stale policy evaluation/persistence races."""

    version: Annotated[int, Field(strict=True, ge=1)]
    operation: Operation


class Publish(Contract):
    """Administrator publishes a complete immutable version atomically."""

    expected_version: Annotated[int, Field(strict=True, ge=1)]
    policy: Policy


class Review(Contract):
    """Independent human acknowledgement, not an external flight approval."""

    decision: Literal["acknowledge", "reject"]
    note: Label
