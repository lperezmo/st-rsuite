/**
 * Convert Python-serialized shortcut ranges into RSuite DateRangePicker
 * `ranges` presets.
 *
 * Each preset arrives as a label plus an ISO [start, end] pair; RSuite wants a
 * label plus a [Date, Date] value. `null` means "not provided", so the caller
 * omits the prop and RSuite keeps its built-in shortcuts (Today / Yesterday /
 * Last 7 days). An empty array is passed through as-is, which removes those
 * defaults and shows no shortcut sidebar.
 */
import type { DateRange } from "rsuite/DateRangePicker";

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

function parseISODate(val: string): Date {
  return new Date(val + "T00:00:00");
}

export function buildRanges(
  ranges: SerializedRange[] | null | undefined
): RangePreset[] | undefined {
  if (ranges == null) return undefined;
  return ranges.map((r) => ({
    label: r.label,
    value: [parseISODate(r.value[0]), parseISODate(r.value[1])] as DateRange,
    closeOverlay: r.closeOverlay,
    placement: r.placement,
  }));
}
