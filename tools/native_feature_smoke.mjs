/** Jason Stys: actual extracted OPA-backed app, real file drafts, holds, publication and independent review. Lines: docs/SOURCE_MAP.md. */
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { chromium, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const [base, output] = process.argv.slice(2);
assert(base && output && process.env.NATIVE_TEST_PASSWORD);
const origin = new URL(base).origin;
const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1440, height: 1000 },
  acceptDownloads: true,
  reducedMotion: "reduce",
});
const page = await context.newPage();
const errors = [],
  external = [],
  statuses = [];
let passed = false;
page.on("response", (response) => {
  if (response.url().startsWith(origin))
    statuses.push({
      path: new URL(response.url()).pathname,
      status: response.status(),
    });
});
page.on("pageerror", (error) => errors.push(error.message));
page.on("request", (request) => {
  if (
    /^https?:/.test(request.url()) &&
    new URL(request.url()).origin !== origin
  )
    external.push(request.url());
});

/** Exercise normal role sign-in; no API cookie injection or preset production accounts. */
async function login(role) {
  await page.goto(base);
  await page.getByLabel("Username", { exact: true }).fill(role);
  await page
    .getByLabel("Password", { exact: true })
    .fill(process.env.NATIVE_TEST_PASSWORD);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(page.locator("#message")).toContainText("Signed in");
  await expect(page.locator("#identity")).toContainText(role);
}

/** Wait for server revocation and UI acknowledgement before another role uses the same browser jar. */
async function logout() {
  const pending = page.waitForResponse(
    (response) =>
      new URL(response.url()).pathname === "/api/logout" &&
      response.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  assert.equal((await pending).status(), 200);
  await expect(page.locator("#message")).toContainText("Signed out");
}

/** Import any supported object as an explicit editor draft through the ordinary user-selected file control. */
async function importFile(kind, value) {
  await page
    .getByLabel(
      `Open ${kind} JSON${kind === "policy" ? " (administrator)" : ""}`,
      { exact: true },
    )
    .setInputFiles({
      name: `${kind}.json`,
      mimeType: "application/json",
      buffer: Buffer.from(JSON.stringify(value)),
    });
  await expect(page.locator("#message")).toContainText(
    "File loaded into draft only",
  );
}

/** Parse a real browser download rather than fabricating the expected report response. */
async function download(name) {
  const pending = page.waitForEvent("download");
  await page.getByRole("button", { name, exact: true }).click();
  const file = await (await pending).path();
  assert(file);
  return JSON.parse(await fs.readFile(file, "utf8"));
}

try {
  await login("admin");
  await expect(page.locator("#application-version")).toContainText("v0.2.1");
  const original = await (
    await page.request.get(new URL("api/workspace", base).href)
  ).json();
  assert.equal(original.version, 1);
  assert.equal(original.history.length, 0);
  const valid = JSON.parse(await page.locator("#operation").inputValue());
  valid.name = "Fictional coastal inspection evidence";
  const missing = structuredClone(valid);
  missing.evidence = missing.evidence.filter(
    (item) => item.fact !== "airspace_authorized",
  );
  await importFile("operation", missing);
  assert.deepEqual(
    JSON.parse(await page.locator("#operation").inputValue()),
    missing,
  );
  assert.deepEqual(
    await (await page.request.get(new URL("api/workspace", base).href)).json(),
    original,
  );
  const evaluation = page.waitForResponse(
    (response) =>
      new URL(response.url()).pathname === "/api/evaluations" &&
      response.request().method() === "POST",
  );
  await page
    .getByRole("button", { name: "Evaluate evidence", exact: true })
    .click();
  assert.equal((await evaluation).status(), 200);
  await expect(page.locator("#report-label")).toContainText("Report 1");
  const held = await download("Export evidence");
  assert.equal(held.result.status, "requires_review");
  assert.equal(held.flight_authorization, false);
  assert.deepEqual(held.operation, missing);
  assert.deepEqual(
    held.result.checks.filter((item) => item.status !== "satisfied"),
    [{ id: "airspace", status: "requires_review", reason: "missing_evidence" }],
  );
  const beforePreview = await (
    await page.request.get(new URL("api/workspace", base).href)
  ).json();
  const draft = structuredClone(original.policy);
  draft.name = "Fictional stricter wind checklist";
  draft.rules.find((rule) => rule.id === "wind").expected = 1;
  await importFile("policy", draft);
  await page
    .getByRole("button", { name: "Preview draft impact", exact: true })
    .click();
  await expect(
    page.getByLabel("Unpublished policy impact", { exact: true }),
  ).toContainText("UNPUBLISHED DRAFT PREVIEW");
  const comparison = await download("Download draft comparison");
  assert.equal(comparison.published, false);
  assert.equal(comparison.before.status, "requires_review");
  assert.equal(comparison.after.status, "blocked");
  const wind = comparison.checks.find((item) => item.id === "wind");
  assert.equal(wind.before.status, "satisfied");
  assert.equal(wind.after.status, "blocked");
  assert.equal(wind.after.reason, "configured_check_failed");
  assert.deepEqual(comparison.draft_policy, draft);
  assert.deepEqual(await download("Download policy draft"), draft);
  assert.deepEqual(
    await (await page.request.get(new URL("api/workspace", base).href)).json(),
    beforePreview,
  );
  await page
    .getByLabel("Unpublished policy impact", { exact: true })
    .screenshot({ path: path.join(output, "01-unpublished-policy-holds.png") });
  const prior = await page.locator("#policy").inputValue();
  await page
    .getByLabel("Open policy JSON (administrator)", { exact: true })
    .setInputFiles({
      name: "invalid.json",
      mimeType: "application/json",
      buffer: Buffer.from([0xc3, 0x28]),
    });
  await expect(page.locator("#message")).toContainText("File not loaded");
  assert.equal(await page.locator("#policy").inputValue(), prior);
  await expect(
    page.getByRole("button", {
      name: "Download draft comparison",
      exact: true,
    }),
  ).toBeDisabled();
  await logout();
  await login("operator");
  await expect(
    page.getByLabel("Open policy JSON (administrator)", { exact: true }),
  ).toBeDisabled();
  await expect(page.locator("#policy")).toHaveAttribute("readonly", "");
  await importFile("operation", valid);
  await page
    .getByRole("button", { name: "Evaluate evidence", exact: true })
    .click();
  await expect(page.locator("#report-label")).toContainText("Report 2");
  const satisfied = await download("Export evidence");
  assert.equal(satisfied.result.status, "satisfied");
  assert(satisfied.result.checks.every((item) => item.status === "satisfied"));
  assert.equal(satisfied.result.flight_authorization, false);
  await logout();
  await login("reviewer");
  await page.getByRole("button", { name: /Report 1 / }).click();
  await expect(
    page.getByRole("button", { name: "Acknowledge evidence", exact: true }),
  ).toBeDisabled();
  await page.getByRole("button", { name: /Report 2 / }).click();
  await expect(
    page.getByRole("button", { name: "Acknowledge evidence", exact: true }),
  ).toBeEnabled();
  await page
    .getByLabel("Review note", { exact: false })
    .fill("Invalid; punctuation");
  await page
    .getByRole("button", { name: "Acknowledge evidence", exact: true })
    .click();
  await expect(page.locator("#message")).toContainText("Review note: use 1-80");
  assert.equal(
    (
      await (
        await page.request.get(new URL("api/evaluations/2", base).href)
      ).json()
    ).review,
    null,
  );
  await page
    .getByLabel("Review note", { exact: false })
    .fill("Independent fictional evidence review. No flight permission.");
  const reviewResponse = page.waitForResponse(
    (response) =>
      new URL(response.url()).pathname === "/api/evaluations/2/review" &&
      response.request().method() === "POST",
  );

  await page
    .getByRole("button", { name: "Acknowledge evidence", exact: true })
    .click();
  assert.equal((await reviewResponse).status(), 200);
  await expect(page.locator("#report-state")).toContainText(
    "Review: acknowledge by reviewer",
  );
  const reviewed = await download("Export evidence");
  assert.equal(reviewed.review.actor, "reviewer");
  assert.equal(reviewed.creator, "operator");
  assert.equal(reviewed.flight_authorization, false);
  await page.locator(".evidence").screenshot({
    path: path.join(output, "02-independent-evidence-review.png"),
  });
  await page.setViewportSize({ width: 390, height: 844 });
  const region = page.getByRole("region", {
    name: "Configured evidence checks",
    exact: true,
  });
  await expect(region).toHaveAttribute("tabindex", "0");
  assert(
    await region.evaluate(
      (element) => element.scrollWidth > element.clientWidth,
    ),
  );
  await region.focus();
  await page.keyboard.press("ArrowRight");
  await expect
    .poll(() => region.evaluate((element) => element.scrollLeft))
    .toBeGreaterThan(0);
  assert.equal(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
    true,
  );
  assert.deepEqual(
    (
      await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
        .analyze()
    ).violations,
    [],
  );
  assert.deepEqual(
    await page.evaluate(() => [localStorage.length, sessionStorage.length]),
    [0, 0],
  );
  const cookies = await context.cookies();
  assert.equal(cookies.length, 1);
  assert.equal(cookies[0].name, process.env.NATIVE_TEST_COOKIE_NAME);
  assert.equal(cookies[0].httpOnly, true);
  assert.equal(cookies[0].sameSite, "Strict");
  assert.deepEqual(external, []);
  assert.deepEqual(errors, []);
  await fs.writeFile(
    path.join(output, "feature.json"),
    JSON.stringify(
      {
        passed: true,
        actual_roles: ["admin", "operator", "reviewer"],
        arbitrary_policy_and_operation_file_drafts: true,
        missing_authorization_holds_exactly_airspace: true,
        lower_wind_cap_blocks_exact_wind_check: true,
        preview_has_no_persistent_writes: true,
        independent_review_preserves_no_flight_permission: true,
        actual_opa_not_python_oracle: true,
        real_evidence_downloads: true,
        mobile_width: 390,
        keyboard_table_scroll: true,
        outside_requests: 0,
      },
      null,
      2,
    ) + "\n",
  );
  passed = true;
} finally {
  const diagnostics = {
    passed,
    statuses,
    errors,
    message: await page
      .locator("#message")
      .textContent()
      .catch(() => "Page closed"),
  };
  await fs.writeFile(
    path.join(output, "browser-diagnostics.json"),
    JSON.stringify(diagnostics, null, 2),
  );
  if (!passed)
    console.error("Native workflow diagnostics:", JSON.stringify(diagnostics));
  await context.close();
  await browser.close();
}
