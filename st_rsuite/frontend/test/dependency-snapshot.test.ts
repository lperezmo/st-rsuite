import { describe, expect, it } from "bun:test";
import {
  packageUrl,
  resolveLock,
  type BunLock,
} from "../scripts/dependency-snapshot";

const lock: BunLock = {
  workspaces: {
    "": {
      dependencies: { "@scope/ui": "^1.0.0" },
      devDependencies: { tool: "^2.0.0" },
    },
  },
  packages: {
    "@scope/ui": [
      "@scope/ui@1.2.0",
      "",
      {
        dependencies: { shared: "^1.0.0", "@scope/internals": "1.0.0" },
        peerDependencies: { react: "^18.0.0", luxon: "^3.0.0" },
        optionalPeers: ["luxon"],
      },
      "sha512-a",
    ],
    "@scope/internals": ["@scope/internals@2.0.0", "", {}, "sha512-b"],
    "@scope/ui/@scope/internals": [
      "@scope/internals@1.0.0",
      "",
      {},
      "sha512-c",
    ],
    shared: ["shared@1.5.0", "", {}, "sha512-d"],
    react: ["react@18.3.1", "", {}, "sha512-e"],
    tool: [
      "tool@2.1.0",
      "",
      { dependencies: { shared: "^1.0.0", helper: "*" } },
      "sha512-f",
    ],
    helper: ["helper@github:someone/helper#abc", "", {}, ""],
  },
};

describe("bun.lock dependency snapshot", () => {
  const resolved = resolveLock(lock);

  it("encodes scoped names in package URLs", () => {
    expect(packageUrl("@scope/ui", "1.2.0")).toBe("pkg:npm/%40scope/ui@1.2.0");
    expect(packageUrl("react", "18.3.1")).toBe("pkg:npm/react@18.3.1");
  });

  it("prefers a nested copy over the hoisted one", () => {
    expect(resolved["@scope/ui"].dependencies).toEqual([
      "pkg:npm/shared@1.5.0",
      "pkg:npm/%40scope/internals@1.0.0",
      "pkg:npm/react@18.3.1",
    ]);
    expect(resolved["@scope/ui/@scope/internals"].package_url).toBe(
      "pkg:npm/%40scope/internals@1.0.0",
    );
  });

  it("marks direct dependencies and runtime reachability", () => {
    expect(resolved["@scope/ui"]).toMatchObject({
      relationship: "direct",
      scope: "runtime",
    });
    expect(resolved.tool).toMatchObject({
      relationship: "direct",
      scope: "development",
    });
    expect(resolved.shared).toMatchObject({
      relationship: "indirect",
      scope: "runtime",
    });
    expect(resolved.react.scope).toBe("runtime");
    // Nothing that ships requires the hoisted copy, only the nested one.
    expect(resolved["@scope/internals"].scope).toBe("development");
  });

  it("leaves out packages that are not from the registry", () => {
    expect(resolved.helper).toBeUndefined();
    expect(resolved.tool.dependencies).toEqual(["pkg:npm/shared@1.5.0"]);
  });
});
