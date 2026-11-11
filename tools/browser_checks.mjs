/** @file Jason Stys: independent real-service browser suites, no auth-throttle bypass or test retries. Lines: docs/SOURCE_MAP.md. */
import { spawnSync } from "node:child_process";
import { randomUUID } from "node:crypto";
import path from "node:path";

// Each engine gets a fresh real service/database. Sharing one 20-attempt/minute loopback
// login budget across all four engines is not representative of independent acceptance suites.
for (const project of ["chromium", "firefox", "webkit", "mobile"]) {
  const result = spawnSync(
    process.execPath,
    [
      path.resolve("node_modules/@playwright/test/cli.js"),
      "test",
      `--project=${project}`,
      ...process.argv.slice(2),
    ],
    {
      stdio: "inherit",
      env: {
        ...process.env,
        POLICY_TEST_DIRECTORY: `.runtime/browser-${project}-${randomUUID()}`,
      },
      timeout: 240000,
    },
  );
  if (result.error || result.status !== 0) {
    console.error(`Browser suite failed: ${project}`);
    process.exit(1);
  }
}
