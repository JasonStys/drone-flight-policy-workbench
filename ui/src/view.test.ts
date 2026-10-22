/** @file Jason Stys: independent status, presentation and review-eligibility regressions; lines: docs/SOURCE_MAP.md. */
import { describe, it, expect } from "vitest";
import {
  canReview,
  counts,
  reasonLabel,
  statusLabel,
  type User,
  type Report,
} from "./view";
const user: User = { name: "reviewer", role: "reviewer", csrf: "synthetic" };
const report: Report = {
  id: 1,
  version: 1,
  creator: "operator",
  stale: false,
  review: null,
  digest: "synthetic",
  operation: {},
  policy: {},
  flight_authorization: false,
  result: {
    status: "satisfied",
    checks: [],
    notice: "synthetic",
    flight_authorization: false,
  },
};
describe("evidence wording and role rules", () => {
  it.each(["satisfied", "blocked", "requires_review"] as const)(
    "labels %s without permission",
    (status) => expect(statusLabel(status)).not.toContain("authorized"),
  );
  it("keeps explanatory text inert", () => {
    expect(reasonLabel("missing_evidence")).toBe("missing evidence");
    expect(reasonLabel("<script>")).toBe("<script>");
  });
  it("counts every status and empty input", () => {
    expect(counts([])).toEqual({
      satisfied: 0,
      blocked: 0,
      requires_review: 0,
    });
    expect(
      counts([
        { id: "a", status: "blocked", reason: "x" },
        { id: "b", status: "satisfied", reason: "x" },
        { id: "c", status: "requires_review", reason: "x" },
      ]),
    ).toEqual({ satisfied: 1, blocked: 1, requires_review: 1 });
  });
  it("allows only independent unreviewed current evidence", () => {
    expect(canReview(user, report, true)).toBe(true);
    expect(canReview({ ...user, role: "admin" }, report, true)).toBe(false);
    expect(canReview(user, { ...report, creator: user.name }, true)).toBe(
      false,
    );
    expect(canReview(user, { ...report, stale: true }, true)).toBe(false);
    expect(
      canReview(
        user,
        {
          ...report,
          review: { actor: "other", decision: "acknowledge", note: "done" },
        },
        true,
      ),
    ).toBe(false);
    expect(
      canReview(
        user,
        { ...report, result: { ...report.result, status: "blocked" } },
        true,
      ),
    ).toBe(false);
    expect(
      canReview(
        user,
        { ...report, result: { ...report.result, status: "requires_review" } },
        true,
      ),
    ).toBe(false);
    expect(
      canReview(
        user,
        { ...report, result: { ...report.result, status: "blocked" } },
        false,
      ),
    ).toBe(true);
  });
});
