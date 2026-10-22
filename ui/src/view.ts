/** @file Jason Stys: pure evidence presentation and review eligibility; exact lines: docs/SOURCE_MAP.md. */
export type Status = "satisfied" | "blocked" | "requires_review";
export interface User {
  name: string;
  role: "admin" | "operator" | "reviewer";
  csrf: string;
}
export interface Check {
  id: string;
  status: Status;
  reason: string;
}
export interface Result {
  status: Status;
  checks: Check[];
  notice: string;
  flight_authorization: false;
}
export interface Report {
  id: number;
  version: number;
  creator: string;
  stale: boolean;
  result: Result;
  review: { actor: string; decision: string; note: string } | null;
  digest: string;
  operation: unknown;
  policy: unknown;
  flight_authorization: false;
}
/** Status wording is intentionally not permission, compliance certification or a safety rating. */
export function statusLabel(status: Status): string {
  return {
    satisfied: "Configured checks satisfied",
    blocked: "Blocked by configured checks",
    requires_review: "Requires evidence review",
  }[status];
}
/** Unknown/private values are never rendered as executable HTML; this returns plain text only. */
export function reasonLabel(reason: string): string {
  return reason.replaceAll("_", " ");
}
/** Independent, fresh, unreviewed evidence is necessary; UI is convenience, server enforces again. */
export function canReview(
  user: User,
  report: Report,
  acknowledge: boolean,
): boolean {
  return (
    user.role === "reviewer" &&
    report.creator !== user.name &&
    !report.stale &&
    report.review === null &&
    (!acknowledge || report.result.status === "satisfied")
  );
}
/** Summarize all rule outcomes without treating skipped or unknown facts as authorization. */
export function counts(checks: Check[]): Record<Status, number> {
  return checks.reduce(
    (sum, row) => {
      sum[row.status] += 1;
      return sum;
    },
    { satisfied: 0, blocked: 0, requires_review: 0 },
  );
}
