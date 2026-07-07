/**
 * Build script that produces a separate Vite library build for each component.
 * Each component gets its own index-[hash].js in its own build/ directory.
 */
import { build } from "vite";
import react from "@vitejs/plugin-react";
import cssInjectedByJsPlugin from "vite-plugin-css-injected-by-js";
import path from "node:path";
import { fileURLToPath } from "node:url";
import process from "node:process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// Production is the default: a bare `npm run build` (locally or in CI) must
// always produce minified bundles without sourcemaps. Dev builds are opt-in
// via `npm run build:dev` / `npm run dev`, which set NODE_ENV=development.
const isProd = process.env.NODE_ENV !== "development";
const isWatch = process.argv.includes("--watch");

const components = [
  { name: "date_input", entry: "./src/date_input/index.tsx" },
  { name: "date_picker", entry: "./src/date_picker/index.tsx" },
  { name: "date_range_input", entry: "./src/date_range_input/index.tsx" },
  { name: "date_range_picker", entry: "./src/date_range_picker/index.tsx" },
  { name: "time_picker", entry: "./src/time_picker/index.tsx" },
  { name: "time_range_picker", entry: "./src/time_range_picker/index.tsx" },
  { name: "radio_tile", entry: "./src/radio_tile/index.tsx" },
  { name: "check_tree", entry: "./src/check_tree/index.tsx" },
  { name: "check_tree_picker", entry: "./src/check_tree_picker/index.tsx" },
  { name: "multi_cascade_tree", entry: "./src/multi_cascade_tree/index.tsx" },
  { name: "carousel", entry: "./src/carousel/index.tsx" },
  { name: "timeline", entry: "./src/timeline/index.tsx" },
  { name: "pin_input", entry: "./src/pin_input/index.tsx" },
];

async function buildComponent(component) {
  const outDir = path.resolve(__dirname, `../${component.name}/frontend/build`);
  console.log(`Building ${component.name} -> ${outDir}`);

  await build({
    root: __dirname,
    base: "./",
    plugins: [react(), cssInjectedByJsPlugin()],
    define: {
      "process.env.NODE_ENV": JSON.stringify(
        process.env.NODE_ENV || "production"
      ),
    },
    build: {
      // Lib-mode ES output skips esbuild whitespace minification (Vite keeps
      // pure annotations intact), so production uses terser for a full minify.
      minify: isProd ? "terser" : false,
      ...(isProd && {
        terserOptions: {
          compress: { drop_console: true, drop_debugger: true },
        },
      }),
      outDir,
      emptyOutDir: true,
      sourcemap: !isProd,
      watch: isWatch ? {} : null,
      lib: {
        entry: component.entry,
        name: component.name,
        formats: ["es"],
        fileName: "index-[hash]",
      },
    },
    logLevel: "info",
  });
}

async function main() {
  for (const component of components) {
    await buildComponent(component);
  }
  console.log("\nAll components built successfully!");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
