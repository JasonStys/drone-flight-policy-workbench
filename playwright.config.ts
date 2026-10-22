/** @file Jason Stys: isolated real SQLite/Python/OPA service browser acceptance; lines: docs/SOURCE_MAP.md. */
import { defineConfig, devices } from "@playwright/test";
import { existsSync } from "node:fs";
import { randomUUID } from "node:crypto";
const directory =
  process.env.POLICY_TEST_DIRECTORY ?? `.runtime/browser-${randomUUID()}`;
process.env.POLICY_TEST_DIRECTORY = directory;
const local =
  process.platform === "win32"
    ? ".venv/Scripts/python.exe"
    : ".venv/bin/python";
const python = process.env.PYTHON ?? (existsSync(local) ? local : "python");
export default defineConfig({
  testDir: "tests/browser",
  timeout: 45000,
  retries: 0,
  workers: 1,
  use: { baseURL: "http://127.0.0.1:8882", trace: "off" },
  webServer: {
    command: `"${python}" -m tools.browser_server --directory "${directory}"`,
    url: "http://127.0.0.1:8882/healthz",
    reuseExistingServer: false,
    timeout: 30000,
  },
  projects: [
    { name: "chromium", use: devices["Desktop Chrome"] },
    { name: "firefox", use: devices["Desktop Firefox"] },
    { name: "webkit", use: devices["Desktop Safari"] },
    { name: "mobile", use: devices["iPhone 13"] },
  ],
});
