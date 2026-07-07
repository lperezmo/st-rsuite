import { FC, useCallback, useMemo } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { DatePicker as RsuiteDatePicker } from "rsuite";
import { useSyncedValue, keyOfScalar } from "../shared/useSyncedValue";
import { buildShouldDisableDate } from "../shared/dateConstraints";

export type DatePickerState = {
  selected_date: string | null;
};

export type DatePickerData = {
  label: string;
  value: string | null;
  format: string;
  appearance: "default" | "subtle";
  size: "lg" | "md" | "sm" | "xs";
  placeholder: string;
  placement: string;
  oneTap: boolean;
  disabled: boolean;
  cleanable: boolean;
  block: boolean;
  isoWeek: boolean;
  showWeekNumbers: boolean;
  editable: boolean;
  loading: boolean;
  minDate?: string | null;
  maxDate?: string | null;
  disabledDates?: string[];
  disabledWeekdays?: number[];
  limitStartYear?: number | null;
  limitEndYear?: number | null;
  calendarDefaultDate?: string | null;
  locale?: string | null;
};

type Props = {
  data: DatePickerData;
  setStateValue: FrontendRendererArgs<
    DatePickerState,
    DatePickerData
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

const DatePickerComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    label,
    value,
    format,
    appearance,
    size,
    placeholder,
    placement,
    oneTap,
    disabled,
    cleanable,
    block,
    isoWeek,
    showWeekNumbers,
    editable,
    loading,
    minDate,
    maxDate,
    disabledDates,
    disabledWeekdays,
    limitStartYear,
    limitEndYear,
    calendarDefaultDate,
  } = data;

  const [selected, emitSelected] = useSyncedValue<Date | null>(
    keyOfScalar(value),
    () => parseDate(value)
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

  const calDefaultDate = useMemo(
    () => (calendarDefaultDate ? parseDate(calendarDefaultDate) ?? undefined : undefined),
    [calendarDefaultDate]
  );

  const handleChange = useCallback(
    (newValue: Date | null) => {
      const iso = toISODate(newValue);
      emitSelected(newValue);
      setStateValue("selected_date", iso);
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
      <RsuiteDatePicker
        value={selected}
        onChange={handleChange}
        format={format}
        appearance={appearance}
        size={size}
        placeholder={placeholder || undefined}
        placement={placement as any}
        oneTap={oneTap}
        disabled={disabled}
        cleanable={cleanable}
        block={block}
        isoWeek={isoWeek}
        showWeekNumbers={showWeekNumbers}
        editable={editable}
        loading={loading}
        shouldDisableDate={shouldDisableDate}
        limitStartYear={limitStartYear ?? undefined}
        limitEndYear={limitEndYear ?? undefined}
        calendarDefaultDate={calDefaultDate}
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default DatePickerComponent;
