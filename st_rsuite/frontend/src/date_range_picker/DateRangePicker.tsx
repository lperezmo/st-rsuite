import { FC, useCallback, useId, useMemo } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { DateRangePicker as RsuiteDateRangePicker } from "rsuite";
import type { DateRange } from "rsuite/DateRangePicker";
import { useSyncedValue, keyOfPair } from "../shared/useSyncedValue";
import { buildShouldDisableDate } from "../shared/dateConstraints";
import { buildRanges, SerializedRange } from "../shared/rangePresets";
import { FieldLabel } from "../shared/FieldLabel";
import { useAnchoredPopup } from "../shared/useAnchoredPopup";
import { toISOValue, parseISOValue } from "../shared/dateValue";

export type DateRangePickerState = {
  start_date: string | null;
  end_date: string | null;
};

export type DateRangePickerData = {
  label: string;
  startValue: string | null;
  endValue: string | null;
  format: string;
  // True when `format` carries a time field, so the widget selects and emits
  // "YYYY-MM-DDTHH:mm:ss" datetimes instead of "YYYY-MM-DD" dates. Derived
  // Python-side from the format string so both sides share one rule.
  withTime: boolean;
  showMeridiem?: boolean;
  character: string;
  appearance: "default" | "subtle";
  size: "lg" | "md" | "sm" | "xs";
  placeholder: string;
  placement: string;
  disabled: boolean;
  cleanable: boolean;
  block: boolean;
  isoWeek: boolean;
  showWeekNumbers: boolean;
  showOneCalendar: boolean;
  oneTap: boolean;
  hoverRange: "week" | "month" | null;
  editable: boolean;
  loading: boolean;
  help?: string | null;
  minDate?: string | null;
  maxDate?: string | null;
  disabledDates?: string[];
  disabledWeekdays?: number[];
  limitStartYear?: number | null;
  limitEndYear?: number | null;
  ranges?: SerializedRange[] | null;
  defaultCalendarValue?: [string, string] | null;
  locale?: string | null;
};

type Props = {
  data: DateRangePickerData;
  setStateValue: FrontendRendererArgs<
    DateRangePickerState,
    DateRangePickerData
  >["setStateValue"];
};

const DateRangePickerComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    label,
    startValue,
    endValue,
    format,
    withTime,
    showMeridiem,
    character,
    appearance,
    size,
    placeholder,
    placement,
    disabled,
    cleanable,
    block,
    isoWeek,
    showWeekNumbers,
    showOneCalendar,
    oneTap,
    hoverRange,
    editable,
    loading,
    help,
    minDate,
    maxDate,
    disabledDates,
    disabledWeekdays,
    limitStartYear,
    limitEndYear,
    ranges,
    defaultCalendarValue,
  } = data;

  const fieldId = useId();
  const popup = useAnchoredPopup(placement);

  const [selected, emitSelected] = useSyncedValue<DateRange | null>(
    keyOfPair(startValue, endValue),
    () => {
      const s = parseISOValue(startValue);
      const e = parseISOValue(endValue);
      return s && e ? [s, e] : null;
    }
  );

  const shouldDisableDate = useMemo(
    () =>
      buildShouldDisableDate({
        minDate,
        maxDate,
        disabledDates,
        disabledWeekdays,
      }),
    [minDate, maxDate, disabledDates, disabledWeekdays]
  );

  const rangePresets = useMemo(() => buildRanges(ranges), [ranges]);
  const defaultCalValue = useMemo<DateRange | undefined>(() => {
    if (!defaultCalendarValue) return undefined;
    const s = parseISOValue(defaultCalendarValue[0]);
    const e = parseISOValue(defaultCalendarValue[1]);
    return s && e ? [s, e] : undefined;
  }, [defaultCalendarValue]);

  const handleChange = useCallback(
    (newValue: DateRange | null) => {
      const s = newValue ? toISOValue(newValue[0], withTime) : null;
      const e = newValue ? toISOValue(newValue[1], withTime) : null;
      emitSelected(newValue);
      setStateValue("start_date", s);
      setStateValue("end_date", e);
    },
    [emitSelected, setStateValue, withTime]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <FieldLabel htmlFor={fieldId} label={label} help={help} />
      <RsuiteDateRangePicker
        id={fieldId}
        value={selected}
        onChange={handleChange}
        format={format}
        character={character}
        appearance={appearance}
        size={size}
        placeholder={placeholder || undefined}
        ref={popup.ref}
        onOpen={popup.onOpen}
        onClose={popup.onClose}
        placement={placement as any}
        disabled={disabled}
        cleanable={cleanable}
        block={block}
        isoWeek={isoWeek}
        showWeekNumbers={showWeekNumbers}
        showOneCalendar={showOneCalendar}
        oneTap={oneTap}
        showMeridiem={showMeridiem}
        hoverRange={hoverRange || undefined}
        editable={editable}
        loading={loading}
        shouldDisableDate={shouldDisableDate}
        limitStartYear={limitStartYear ?? undefined}
        limitEndYear={limitEndYear ?? undefined}
        ranges={rangePresets}
        defaultCalendarValue={defaultCalValue}
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default DateRangePickerComponent;
