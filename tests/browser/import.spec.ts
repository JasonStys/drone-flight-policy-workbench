/** Jason Stys: real OPA-backed file drafts, exact downloads, roles and stale file completion. Lines: docs/SOURCE_MAP.md. */
import { test, expect, type Page } from "@playwright/test";
import fs from "node:fs/promises";
import AxeBuilder from "@axe-core/playwright";

declare global {
  interface Window {
    __heldImport?: boolean;
    __releaseImport?: () => void;
  }
}

/** Sign into only this test's new random synthetic account directory. */
async function login(page: Page, role = "admin"): Promise<void> {
  const accounts = JSON.parse(
    await fs.readFile(
      `${process.env.POLICY_TEST_DIRECTORY}/credentials.json`,
      "utf8",
    ),
  );
  await page.goto("/");
  await page
    .getByLabel("Username", { exact: true })
    .fill(accounts[role].username);
  await page
    .getByLabel("Password", { exact: true })
    .fill(accounts[role].password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(page.locator("#message")).toContainText("Signed in");
}

test("selected operation/policy files remain drafts, preview exact holds and download exact intended data", async ({
  page,
}) => {
  await login(page);
  const original = await (await page.request.get("/api/workspace")).json();
  const policy = structuredClone(original.policy);
  policy.name = "Fictional one-metre-per-second organizational wind cap";
  policy.rules.find((rule: { id: string }) => rule.id === "wind").expected = 1;
  const operation = JSON.parse(await page.locator("#operation").inputValue());
  operation.name = "Fictional imported inspection evidence";
  for (const [kind, value] of [
    ["policy", policy],
    ["operation", operation],
  ] as const) {
    await page.locator(`#${kind}-file`).setInputFiles({
      name: `${kind}.json`,
      mimeType: "application/json",
      buffer: Buffer.from(JSON.stringify({ [kind]: value })),
    });
    await expect(page.locator("#message")).toContainText(
      "File loaded into draft only",
    );
    expect(JSON.parse(await page.locator(`#${kind}`).inputValue())).toEqual(
      value,
    );
    const pending = page.waitForEvent("download");
    await page
      .getByRole("button", { name: `Download ${kind} draft`, exact: true })
      .click();
    const file = await (await pending).path();
    if (!file) throw new Error("Actual browser download missing");
    expect(JSON.parse(await fs.readFile(file, "utf8"))).toEqual(value);
  }
  await page
    .getByRole("button", { name: "Preview draft impact", exact: true })
    .click();
  await expect(
    page.getByLabel("Unpublished policy impact", { exact: true }),
  ).toContainText("wind:");
  expect(await (await page.request.get("/api/workspace")).json()).toEqual(
    original,
  );
  const retained = await page.locator("#policy").inputValue();
  for (const buffer of [
    Buffer.from([0xc3, 0x28]),
    Buffer.from("[]"),
    Buffer.from('{"number":1e999}'),
  ]) {
    await page.locator("#policy-file").setInputFiles({
      name: "invalid.json",
      mimeType: "application/json",
      buffer,
    });
    await expect(page.locator("#message")).toContainText("File not loaded");
    await expect(
      page.getByRole("button", {
        name: "Download draft comparison",
        exact: true,
      }),
    ).toBeDisabled();
    expect(await page.locator("#policy").inputValue()).toBe(retained);
  }
  await page.setViewportSize({ width: 390, height: 844 });
  const help = page
    .locator("summary")
    .filter({ hasText: "How to interpret this workbench" });
  const helpBox = await help.boundingBox();
  if (!helpBox) throw new Error("Visible help control missing");
  expect(helpBox.height).toBeGreaterThanOrEqual(24);
  await help.focus();
  await page.keyboard.press("Enter");
  await expect(help.locator("..")).toHaveAttribute("open", "");
  expect(
    (
      await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
        .analyze()
    ).violations,
  ).toEqual([]);
});

test("late file completion cannot replace typing, a newer choice, refresh or a signed-out context", async ({
  page,
}) => {
  await login(page);
  await page.evaluate(() => {
    const original = File.prototype.arrayBuffer;
    File.prototype.arrayBuffer = function () {
      if (!this.name.startsWith("held-")) return original.call(this);
      window.__heldImport = true;
      return new Promise<ArrayBuffer>((resolve, reject) => {
        window.__releaseImport = () => {
          void original.call(this).then(resolve, reject);
        };
      });
    };
  });
  const original = JSON.parse(await page.locator("#policy").inputValue());
  const older = { ...original, name: "Delayed old policy file" };
  const newer = { ...original, name: "Newer explicit policy choice" };
  async function hold(): Promise<void> {
    await page.evaluate(() => {
      window.__heldImport = false;
    });
    await page.locator("#policy-file").setInputFiles({
      name: "held-policy.json",
      mimeType: "application/json",
      buffer: Buffer.from(JSON.stringify(older)),
    });
    await page.waitForFunction(() => window.__heldImport === true);
  }
  await hold();
  await page.locator("#policy").fill(JSON.stringify(newer));
  await page.evaluate(() => window.__releaseImport?.());
  expect(JSON.parse(await page.locator("#policy").inputValue())).toEqual(newer);
  await hold();
  await page.locator("#policy-file").setInputFiles({
    name: "newer.json",
    mimeType: "application/json",
    buffer: Buffer.from(JSON.stringify(newer)),
  });
  await expect(page.locator("#message")).toContainText(
    "File loaded into draft only",
  );
  await page.evaluate(() => window.__releaseImport?.());
  expect(JSON.parse(await page.locator("#policy").inputValue())).toEqual(newer);
  await hold();
  await page
    .getByRole("button", { name: "Refresh workspace", exact: true })
    .click();
  await expect(page.locator("#message")).toContainText("Workspace refreshed");
  await page.evaluate(() => window.__releaseImport?.());
  expect(JSON.parse(await page.locator("#policy").inputValue())).toEqual(
    original,
  );
  await hold();
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await expect(page.locator("#message")).toContainText("Signed out");
  await page.evaluate(() => window.__releaseImport?.());
  await expect(page.locator("#policy")).toHaveValue("");
  await expect(page.locator("#message")).toContainText("Signed out");
});

test("an operator cannot load policy standards through a manually dispatched file event", async ({
  page,
}) => {
  await login(page, "operator");
  const original = await (await page.request.get("/api/workspace")).json();
  const retained = await page.locator("#policy").inputValue();
  await expect(page.locator("#policy-file")).toBeDisabled();
  await page.locator("#policy-file").setInputFiles({
    name: "unapproved.json",
    mimeType: "application/json",
    buffer: Buffer.from('{"name":"Unapproved policy"}'),
  });
  expect(await page.locator("#policy").inputValue()).toBe(retained);
  expect(await (await page.request.get("/api/workspace")).json()).toEqual(
    original,
  );
});
