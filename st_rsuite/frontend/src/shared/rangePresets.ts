/**
 * Convert Python-serialized shortcut ranges into RSuite DateRangePicker
 * `ranges` presets.
 *
 * Each preset arrives as a label plus an ISO [start, end] pair (a plain date,
 * or a date-time when the picker is in datetime mode); RSuite wants a
 * label plus a [Date, Date] value. `null` means "not provided", so the caller
 * omits the prop and RSuite keeps its built-in shortcuts (Today / Yesterday /
 * Last 7 days). An empty array is passed through as-is, which removes those
 * defaults and shows no shortcut sidebar.
 */
import type { DateRange } from "rsuite/DateRangePicker";
import { parseISOValue } from "./dateValue";

export type SerializedRange = {
  label: string;
  value: [string, string];
  closeOverlay?: boolean;
  placement?: "bottom" | "left";
};

type RangePreset = {
  label: string;
  value: DateRange;
  closeOverlay?: boolean;
  placement?: "bottom" | "left";
};

export function buildRanges(
  ranges: SerializedRange[] | null | undefined,
): RangePreset[] | undefined {
  if (ranges == null) return undefined;
  const presets: RangePreset[] = [];
  for (const r of ranges) {
    const start = parseISOValue(r.value[0]);
    const end = parseISOValue(r.value[1]);
    // A preset whose ends do not parse would hand RSuite a null range; skip
    // it rather than render a shortcut that selects nothing.
    if (!start || !end) continue;
    const value: DateRange = [start, end];
    presets.push({
      label: r.label,
      value,
      closeOverlay: r.closeOverlay,
      placement: r.placement,
    });
  }
  return presets;
}
