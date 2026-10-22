/** @file Jason Stys: real native-backed role, evidence, policy-history and accessibility journeys. Lines: docs/SOURCE_MAP.md. */
import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import fs from "node:fs";
/** Read only randomly generated local test credentials; never committed or used against real services. */
async function login(page: Page, role: string): Promise<void> {
  const credentials = JSON.parse(
    fs.readFileSync(
      `${process.env.POLICY_TEST_DIRECTORY}/credentials.json`,
      "utf8",
    ),
  )[role];
  await page.goto("/");
  await page.getByLabel("Username", { exact: true }).fill(credentials.username);
  await page.getByLabel("Password", { exact: true }).fill(credentials.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(page.locator("#message")).toContainText("Signed in");
}
test("operator evaluates all three statuses, exports and invalidates edits", async ({
  page,
}) => {
  await login(page, "operator");
  await expect(page.locator("#policy")).not.toBeEditable();
  await expect(
    page.getByRole("button", { name: "Publish policy version" }),
  ).toBeDisabled();
  await page.getByRole("button", { name: "Evaluate evidence" }).click();
  await expect(page.locator("#message")).toContainText("Evaluation saved");
  await expect(page.locator("#outcome")).toContainText(
    "Configured checks satisfied",
  );
  const download = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export evidence" }).click();
  expect((await download).suggestedFilename()).toMatch(
    /^policy-evidence-\d+\.json$/,
  );
  for (const [value, label] of [
    ["missing-approval", "Requires evidence review"],
    ["privacy-hold", "Blocked by configured checks"],
    ["expired-record", "Blocked by configured checks"],
  ]) {
    await page.locator("#scenario").selectOption(value);
    await expect(
      page.getByRole("button", { name: "Export evidence" }),
    ).toBeDisabled();
    await page.getByRole("button", { name: "Evaluate evidence" }).click();
    await expect(page.locator("#message")).toContainText("Evaluation saved");
    await expect(page.locator("#outcome")).toContainText(label);
  }
  await page.locator("#operation").fill("{invalid}");
  await expect(page.locator("#checks")).toBeEmpty();
  await page.getByRole("button", { name: "Evaluate evidence" }).click();
  await expect(page.locator("#message")).toContainText("Request failed");
  await expect(
    page.getByRole("button", { name: "Export evidence" }),
  ).toBeDisabled();
  // Hold a real final report GET, not just the initial evaluation POST.
  const changed = '{"name":"Late draft retained","as_of_s":1000,"evidence":[]}';
  await page.locator("#scenario").selectOption("inspection");
  let releaseReport!: () => void;
  let enteredReport!: () => void;
  const reportStarted = new Promise<void>((resolve) => {
    enteredReport = resolve;
  });
  const reportGate = new Promise<void>((resolve) => {
    releaseReport = resolve;
  });
  await page.route(
    "**/api/evaluations/*",
    async (route) => {
      enteredReport();
      await reportGate;
      await route.continue();
    },
    { times: 1 },
  );
  await page.getByRole("button", { name: "Evaluate evidence" }).click();
  await reportStarted;
  await page.locator("#operation").fill(changed);
  releaseReport();
  await expect(page.locator("#message")).toContainText(
    "Draft changed during report loading",
  );
  await expect(page.locator("#operation")).toHaveValue(changed);
  await expect(page.locator("#checks")).toBeEmpty();
  await expect(
    page.getByRole("button", { name: "Export evidence" }),
  ).toBeDisabled();
});
test("admin publishes immutable policy; history is stale and independent reviewer cannot override", async ({
  page,
}) => {
  await login(page, "admin");
  await page.getByRole("button", { name: "Evaluate evidence" }).click();
  await expect(page.locator("#message")).toContainText("Evaluation saved");
  const historyButton = await page
    .locator("#history button")
    .first()
    .innerText();
  const policy = JSON.parse(await page.locator("#policy").inputValue());
  policy.name = "Browser-reviewed organization policy";
  await page.locator("#policy").fill(JSON.stringify(policy));
  await page.getByRole("button", { name: "Publish policy version" }).click();
  await expect(page.locator("#message")).toContainText(
    "New immutable policy version published",
  );
  await page.getByRole("button", { name: historyButton, exact: true }).click();
  await expect(page.locator("#report-state")).toContainText("STALE POLICY");
  await page.getByRole("button", { name: "Evaluate evidence" }).click();
  await expect(page.locator("#message")).toContainText("Evaluation saved");
  const currentReport = await page
    .locator("#history button")
    .first()
    .innerText();
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await expect(page.locator("#message")).toContainText("Signed out");
  await login(page, "reviewer");
  await page.getByRole("button", { name: historyButton, exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Acknowledge evidence" }),
  ).toBeDisabled();
  await page.getByRole("button", { name: currentReport, exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Acknowledge evidence" }),
  ).toBeEnabled();
  await page.getByRole("button", { name: "Acknowledge evidence" }).click();
  await expect(page.locator("#message")).toContainText(
    "Independent review recorded",
  );
  await expect(page.locator("#report-state")).toContainText(
    "acknowledge by demo-reviewer",
  );
  await expect(
    page.getByRole("button", { name: "Acknowledge evidence" }),
  ).toBeDisabled();
  await expect(
    page.getByRole("button", { name: "Record rejection" }),
  ).toBeDisabled();
  const operatorReport = page
    .locator("#history button")
    .filter({ hasText: "demo-operator" })
    .first();
  await operatorReport.click();
  await expect(
    page.getByRole("button", { name: "Acknowledge evidence" }),
  ).toBeDisabled();
  await page
    .getByText("How to interpret this workbench", { exact: true })
    .click();
  expect(
    (
      await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
        .analyze()
    ).violations,
  ).toEqual([]);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBeTruthy();
});
test("in-flight draft edit cannot restore obsolete evidence", async ({
  page,
}) => {
  await login(page, "operator");
  let release!: () => void;
  let entered!: () => void;
  const started = new Promise<void>((resolve) => {
    entered = resolve;
  });
  const gate = new Promise<void>((resolve) => {
    release = resolve;
  });
  await page.route(
    "**/api/evaluations",
    async (route) => {
      entered();
      await gate;
      await route.continue();
    },
    { times: 1 },
  );
  await page.getByRole("button", { name: "Evaluate evidence" }).click();
  await started;
  const changed = '{"name":"Draft retained","as_of_s":1000,"evidence":[]}';
  await page.locator("#operation").fill(changed);
  release();
  await expect(page.locator("#message")).toContainText(
    "Draft changed during evaluation",
  );
  await expect(page.locator("#operation")).toHaveValue(changed);
  await expect(page.locator("#checks")).toBeEmpty();
  await expect(
    page.getByRole("button", { name: "Export evidence" }),
  ).toBeDisabled();
});
