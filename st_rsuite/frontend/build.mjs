/**
 * Build script that produces ONE Vite library build shared by all widgets.
 * The single entry (src/index.tsx) routes on data.kind; locales split into
 * lazy chunks so a page only downloads the locale it renders.
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

const outDir = path.resolve(__dirname, "build");

async function main() {
  console.log(`Building st-rsuite bundle -> ${outDir}`);

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
        entry: "./src/index.tsx",
        name: "st_rsuite",
        formats: ["es"],
        fileName: "index-[hash]",
      },
      rollupOptions: {
        output: {
          // The Python side registers js="index-*.js", which must match
          // exactly one file: lazy chunks must not collide with that glob.
          chunkFileNames: "chunk-[name]-[hash].js",
        },
      },
    },
    logLevel: "info",
  });

  console.log("\nBundle built successfully!");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
