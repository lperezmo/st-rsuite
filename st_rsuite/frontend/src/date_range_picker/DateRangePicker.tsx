import { FC, useCallback, useMemo } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { DateRangePicker as RsuiteDateRangePicker } from "rsuite";
import type { DateRange } from "rsuite/DateRangePicker";
import { useSyncedValue, keyOfPair } from "../shared/useSyncedValue";
import { buildShouldDisableDate } from "../shared/dateConstraints";

export type DateRangePickerState = {
  start_date: string | null;
  end_date: string | null;
};

export type DateRangePickerData = {
  label: string;
  startValue: string | null;
  endValue: string | null;
  format: string;
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
  minDate?: string | null;
  maxDate?: string | null;
  disabledDates?: string[];
  disabledWeekdays?: number[];
  limitStartYear?: number | null;
  limitEndYear?: number | null;
  locale?: string | null;
};

type Props = {
  data: DateRangePickerData;
  setStateValue: FrontendRendererArgs<
    DateRangePickerState,
    DateRangePickerData
  >["setStateValue"];
};

function toISODate(d: Date | null): string | null {
  if (!d || isNaN(d.getTime())) return null;
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function parseDate(val: string | null): Date | null {
  if (!val) return null;
  const d = new Date(val + "T00:00:00");
  return isNaN(d.getTime()) ? null : d;
}

const DateRangePickerComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    label,
    startValue,
    endValue,
    format,
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
    minDate,
    maxDate,
    disabledDates,
    disabledWeekdays,
    limitStartYear,
    limitEndYear,
  } = data;

  const [selected, emitSelected] = useSyncedValue<DateRange | null>(
    keyOfPair(startValue, endValue),
    () => {
      const s = parseDate(startValue);
      const e = parseDate(endValue);
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

  const handleChange = useCallback(
    (newValue: DateRange | null) => {
      const s = newValue ? toISODate(newValue[0]) : null;
      const e = newValue ? toISODate(newValue[1]) : null;
      emitSelected(newValue);
      setStateValue("start_date", s);
      setStateValue("end_date", e);
    },
    [emitSelected, setStateValue]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      {label && (
        <label
          style={{
            display: "block",
            marginBottom: 4,
            fontSize: 14,
            fontWeight: 500,
          }}
        >
          {label}
        </label>
      )}
      <RsuiteDateRangePicker
        value={selected}
        onChange={handleChange}
        format={format}
        character={character}
        appearance={appearance}
        size={size}
        placeholder={placeholder || undefined}
        placement={placement as any}
        disabled={disabled}
        cleanable={cleanable}
        block={block}
        isoWeek={isoWeek}
        showWeekNumbers={showWeekNumbers}
        showOneCalendar={showOneCalendar}
        oneTap={oneTap}
        hoverRange={hoverRange || undefined}
        editable={editable}
        loading={loading}
        shouldDisableDate={shouldDisableDate}
        limitStartYear={limitStartYear ?? undefined}
        limitEndYear={limitEndYear ?? undefined}
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default DateRangePickerComponent;
