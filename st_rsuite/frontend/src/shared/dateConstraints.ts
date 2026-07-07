/**
 * Build an RSuite `shouldDisableDate` predicate from declarative constraints.
 *
 * A callable cannot cross the Python/JS boundary, so the Python wrappers send
 * plain data (ISO date bounds, an explicit disabled list, disabled weekdays)
 * and this reconstructs the predicate RSuite's DatePicker / DateRangePicker
 * expect. Returns `undefined` when no constraint is set, so the component can
 * omit the prop entirely and keep RSuite's default (every date enabled).
 */

export type DateConstraints = {
  minDate?: string | null;
  maxDate?: string | null;
  disabledDates?: string[];
  // Weekdays to disable, 0 = Monday .. 6 = Sunday (matching Python's
  // date.weekday()), NOT JavaScript's Sunday-first getDay().
  disabledWeekdays?: number[];
};

function toISODate(d: Date): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function parseISODate(val: string): Date | null {
  const d = new Date(val + "T00:00:00");
  return isNaN(d.getTime()) ? null : d;
}

export function buildShouldDisableDate(
  c: DateConstraints
): ((date: Date) => boolean) | undefined {
  const min = c.minDate ? parseISODate(c.minDate) : null;
  const max = c.maxDate ? parseISODate(c.maxDate) : null;
  const disabled = new Set(c.disabledDates ?? []);
  const weekdays = new Set(c.disabledWeekdays ?? []);

  if (!min && !max && disabled.size === 0 && weekdays.size === 0) {
    return undefined;
  }

  return (date: Date) => {
    if (!date || isNaN(date.getTime())) return false;
    // Compare on calendar day only, ignoring any time component.
    const day = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    if (min && day < min) return true;
    if (max && day > max) return true;
    if (disabled.has(toISODate(day))) return true;
    // Convert JS Sunday-first getDay() to Python Monday-first weekday().
    const mondayFirst = (date.getDay() + 6) % 7;
    if (weekdays.has(mondayFirst)) return true;
    return false;
  };
}
