/**
 * Two-way value sync between Python and a controlled RSuite component.
 *
 * The naive pattern (`useState(initialValue)`) hydrates local state once and
 * never reconciles, so any later change to the Python-side `value=` is silently
 * ignored: reset buttons, dependent widgets, and Session-State-driven updates
 * all fail. This hook keeps local state as the source of truth for user edits
 * while still adopting Python-driven changes.
 *
 * The mechanism is a canonical string key. The component reduces the incoming
 * Python value to a stable string (an ISO date, a joined list, etc.). The hook
 * remembers the last incoming key it saw and, on each render, adopts the new
 * value only when that incoming key actually changes:
 *
 * - Incoming key changed  -> Python drove a new value, so adopt it.
 * - Incoming key unchanged -> nothing new from Python; keep local state, which
 *   preserves any edit the user made since the last render.
 *
 * Crucially the remembered key tracks the *incoming* value only, never what the
 * user emitted. If it also moved on user edits, a static `value=` (unchanged
 * across reruns) would look different from the user's last emission and get
 * re-adopted every rerun, reverting the edit. Tracking incoming alone also
 * means that when the app does feed the widget's output back into `value=`
 * (the controlled pattern), the echo carries the value the user just produced,
 * so adopting it is a no-op and never fights an in-progress edit.
 */
import { useCallback, useEffect, useRef, useState } from "react";

export function useSyncedValue<T>(
  incomingKey: string,
  parseIncoming: () => T,
): [T, (next: T) => void] {
  // Keep the latest parse closure without making it an effect dependency, so a
  // new closure each render does not re-run the sync effect on its own.
  const parseRef = useRef(parseIncoming);
  parseRef.current = parseIncoming;

  const [value, setValue] = useState<T>(() => parseRef.current());
  const lastIncomingKey = useRef<string>(incomingKey);

  useEffect(() => {
    if (incomingKey !== lastIncomingKey.current) {
      lastIncomingKey.current = incomingKey;
      setValue(parseRef.current());
    }
  }, [incomingKey]);

  const setLocal = useCallback((next: T) => {
    setValue(next);
  }, []);

  return [value, setLocal];
}

/** Canonical key for a single nullable string (ISO date/time, selected value). */
export function keyOfScalar(v: string | null | undefined): string {
  return v ?? "";
}

/** Canonical key for a (start, end) pair of nullable strings. */
export function keyOfPair(
  start: string | null | undefined,
  end: string | null | undefined,
): string {
  return `${start ?? ""}|${end ?? ""}`;
}

/**
 * Canonical key for a list of string values (order-sensitive). Joined on NUL,
 * which cannot occur in these values, so distinct lists never collide. A space
 * separator would collide: the values are free-form (tag_picker is creatable),
 * so ["New York"] and ["New", "York"] would key alike, and a Python-driven
 * change between them would be silently ignored.
 *
 * The separator is written as an escape rather than a literal NUL byte. A raw
 * NUL makes the file read as binary to git and to text tooling, which hides
 * both the separator and this whole function from review.
 */
export function keyOfList(values: string[] | null | undefined): string {
  return (values ?? []).join("\u0000");
}
