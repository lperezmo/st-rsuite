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
const isProd = process.env.NODE_ENV === "production";
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
      minify: isProd ? "esbuild" : false,
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
      ...(isProd && {
        esbuild: {
          drop: ["console", "debugger"],
          minifyIdentifiers: true,
          minifySyntax: true,
          minifyWhitespace: true,
        },
      }),
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
