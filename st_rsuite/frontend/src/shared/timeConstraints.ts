/**
 * Build RSuite `hideHours` / `hideMinutes` / `hideSeconds` predicates from
 * declarative constraints.
 *
 * The standalone TimePicker / TimeRangePicker expose only the *hide* family
 * (there is no shouldDisableHour on them, unlike DatePicker in time mode), so a
 * hidden unit is removed from the scroll panel entirely. A callable cannot cross
 * the Python/JS boundary, so the wrappers send plain lists plus an optional hour
 * window and this reconstructs the predicates. Each builder returns `undefined`
 * when nothing is constrained, so the component omits the prop and RSuite keeps
 * every unit visible.
 */

export type TimeConstraints = {
  hiddenHours?: number[];
  hiddenMinutes?: number[];
  hiddenSeconds?: number[];
  // Inclusive hour window; hours outside it are hidden. Convenience for
  // business-hours pickers, on top of any explicit hiddenHours.
  minHour?: number | null;
  maxHour?: number | null;
};

export function buildHideHours(
  c: TimeConstraints
): ((hour: number) => boolean) | undefined {
  const hidden = new Set(c.hiddenHours ?? []);
  const hasWindow = c.minHour != null || c.maxHour != null;
  if (hidden.size === 0 && !hasWindow) return undefined;
  return (hour: number) => {
    if (hidden.has(hour)) return true;
    if (c.minHour != null && hour < c.minHour) return true;
    if (c.maxHour != null && hour > c.maxHour) return true;
    return false;
  };
}

export function buildHideMinutes(
  c: TimeConstraints
): ((minute: number) => boolean) | undefined {
  const hidden = new Set(c.hiddenMinutes ?? []);
  if (hidden.size === 0) return undefined;
  return (minute: number) => hidden.has(minute);
}

export function buildHideSeconds(
  c: TimeConstraints
): ((second: number) => boolean) | undefined {
  const hidden = new Set(c.hiddenSeconds ?? []);
  if (hidden.size === 0) return undefined;
  return (second: number) => hidden.has(second);
}
