/**
 * Serialization shared by the date-flavored pickers.
 *
 * The pickers speak two shapes to Python, chosen by the `withTime` flag the
 * Python wrapper derives from the `format` string:
 *
 * - date mode     -> "YYYY-MM-DD"
 * - datetime mode -> "YYYY-MM-DDTHH:mm:ss"
 *
 * Both are local wall time with no timezone suffix, so a value does not shift
 * a day (or an hour) on the way across, with the one exception of a wall time
 * that does not exist locally (inside a DST spring-forward gap), which the
 * browser normalizes forward. Seconds are always present in datetime
 * mode even when the format shows only hours and minutes, which keeps the shape
 * fixed for Python's `datetime.fromisoformat`.
 */

function pad(n: number): string {
  return String(n).padStart(2, "0");
}

/** Serialize a Date for Python. `withTime` picks the shape. */
export function toISOValue(d: Date | null, withTime: boolean): string | null {
  if (!d || isNaN(d.getTime())) return null;
  const day = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  if (!withTime) return day;
  const time = `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
  return `${day}T${time}`;
}

/**
 * Parse a value coming from Python. Accepts both shapes regardless of mode: a
 * bare "YYYY-MM-DD" in datetime mode lands at midnight, and a timestamp in date
 * mode simply keeps a time nothing reads. Parsed as local time (no "Z"), which
 * is what `new Date` does for both shapes.
 */
export function parseISOValue(val: string | null | undefined): Date | null {
  if (!val) return null;
  const text = val.includes("T") ? val : `${val}T00:00:00`;
  const d = new Date(text);
  return isNaN(d.getTime()) ? null : d;
}
