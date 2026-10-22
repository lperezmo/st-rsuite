/**
 * Turns bun.lock into a GitHub dependency submission snapshot.
 *
 * GitHub's dependency graph reads package-lock.json, yarn.lock and
 * pnpm-lock.yaml but not bun.lock, so without this it only sees the ranges in
 * package.json and Dependabot alerts miss every transitive package. The
 * dependency-snapshot workflow posts this script's output to
 * POST /repos/{owner}/{repo}/dependency-graph/snapshots.
 *
 * It reads the lockfile only: nothing is installed or fetched.
 *
 *   bun scripts/dependency-snapshot.ts > snapshot.json
 */

const LOCKFILE_PATH = "st_rsuite/frontend/bun.lock";

type PackageEntry = [
  id: string,
  registry: string,
  info?: {
    dependencies?: Record<string, string>;
    optionalDependencies?: Record<string, string>;
    peerDependencies?: Record<string, string>;
    optionalPeers?: string[];
  },
  integrity?: string,
];

export type BunLock = {
  workspaces: Record<
    string,
    {
      dependencies?: Record<string, string>;
      devDependencies?: Record<string, string>;
      optionalDependencies?: Record<string, string>;
    }
  >;
  packages: Record<string, PackageEntry>;
};

export type ResolvedDependency = {
  package_url: string;
  relationship: "direct" | "indirect";
  scope: "runtime" | "development";
  dependencies: string[];
};

/** "@a/b/c/@d/e" -> ["@a/b", "c", "@d/e"] */
function splitKey(key: string): string[] {
  const parts: string[] = [];
  const tokens = key.split("/");
  for (let i = 0; i < tokens.length; i++) {
    parts.push(
      tokens[i].startsWith("@") ? `${tokens[i]}/${tokens[++i]}` : tokens[i],
    );
  }
  return parts;
}

/** Splits "name@version", where the name itself may start with "@". */
function parseId(id: string): { name: string; version: string } {
  const at = id.lastIndexOf("@");
  return { name: id.slice(0, at), version: id.slice(at + 1) };
}

export function packageUrl(name: string, version: string): string {
  return `pkg:npm/${name.replace(/^@/, "%40")}@${version}`;
}

/**
 * Resolves a dependency name the way node_modules lookup does: the nearest
 * nested copy under the requiring package's path wins, then each parent's,
 * then the hoisted one.
 */
function resolve(packages: BunLock["packages"], fromKey: string, name: string) {
  const path = fromKey ? splitKey(fromKey) : [];
  for (let depth = path.length; depth >= 0; depth--) {
    const key = [...path.slice(0, depth), name].join("/");
    if (key in packages) return key;
  }
  return undefined;
}

function childNames(entry: PackageEntry): string[] {
  const info = entry[2] ?? {};
  const optionalPeers = new Set(info.optionalPeers ?? []);
  return [
    ...Object.keys(info.dependencies ?? {}),
    ...Object.keys(info.optionalDependencies ?? {}),
    ...Object.keys(info.peerDependencies ?? {}).filter(
      (name) => !optionalPeers.has(name),
    ),
  ];
}

export function resolveLock(lock: BunLock): Record<string, ResolvedDependency> {
  const { packages } = lock;
  const root = lock.workspaces[""] ?? {};
  const runtimeRoots = [
    ...Object.keys(root.dependencies ?? {}),
    ...Object.keys(root.optionalDependencies ?? {}),
  ];
  const direct = new Set([
    ...runtimeRoots,
    ...Object.keys(root.devDependencies ?? {}),
  ]);

  // Only registry packages have a version a vulnerability advisory can match.
  const isRegistryPackage = (key: string) =>
    /^\d/.test(parseId(packages[key][0]).version);

  const children = new Map<string, string[]>();
  for (const key of Object.keys(packages)) {
    const resolved = childNames(packages[key])
      .map((name) => resolve(packages, key, name))
      .filter((child): child is string => child !== undefined);
    children.set(key, resolved);
  }

  // Anything reachable from a runtime dependency ships in the bundles.
  const runtime = new Set<string>();
  const pending = runtimeRoots
    .map((name) => resolve(packages, "", name))
    .filter((key): key is string => key !== undefined);
  while (pending.length > 0) {
    const key = pending.pop()!;
    if (runtime.has(key)) continue;
    runtime.add(key);
    pending.push(...(children.get(key) ?? []));
  }

  const resolved: Record<string, ResolvedDependency> = {};
  for (const key of Object.keys(packages)) {
    if (!isRegistryPackage(key)) continue;
    const { name, version } = parseId(packages[key][0]);
    resolved[key] = {
      package_url: packageUrl(name, version),
      relationship: direct.has(key) ? "direct" : "indirect",
      scope: runtime.has(key) ? "runtime" : "development",
      dependencies: (children.get(key) ?? [])
        .filter(isRegistryPackage)
        .map((child) => {
          const { name, version } = parseId(packages[child][0]);
          return packageUrl(name, version);
        }),
    };
  }
  return resolved;
}

if (import.meta.main) {
  const lock = Bun.JSONC.parse(
    await Bun.file(new URL("../bun.lock", import.meta.url)).text(),
  ) as BunLock;
  const env = process.env;
  const snapshot = {
    version: 0,
    sha: env.GITHUB_SHA ?? "0000000000000000000000000000000000000000",
    ref: env.GITHUB_REF ?? "refs/heads/main",
    job: {
      // One correlator per lockfile, so each run replaces the last snapshot.
      correlator: `${env.GITHUB_WORKFLOW ?? "local"}_${LOCKFILE_PATH}`,
      id: env.GITHUB_RUN_ID ?? "local",
    },
    detector: {
      name: "st-rsuite bun.lock snapshot",
      version: "1.0.0",
      url: "https://github.com/lperezmo/st-rsuite/blob/main/st_rsuite/frontend/scripts/dependency-snapshot.ts",
    },
    scanned: new Date().toISOString(),
    manifests: {
      [LOCKFILE_PATH]: {
        name: LOCKFILE_PATH,
        file: { source_location: LOCKFILE_PATH },
        resolved: resolveLock(lock),
      },
    },
  };
  console.log(JSON.stringify(snapshot, null, 2));
}
