/** @file Jason Stys: static production build and presentation-helper coverage gates. Lines: docs/SOURCE_MAP.md. */
import pkg from "./package.json" with { type: "json" };
import { defineConfig } from "vitest/config";
export default defineConfig({
  define: { __APP_VERSION__: JSON.stringify(pkg.version) },
  root: "ui",
  build: { outDir: "../dist", emptyOutDir: true },
  test: {
    include: ["src/*.test.ts"],
    coverage: {
      provider: "v8",
      include: ["src/view.ts", "src/import_file.ts"],
      thresholds: {
        lines: 100,
        branches: 100,
        functions: 100,
        statements: 100,
      },
    },
  },
});
