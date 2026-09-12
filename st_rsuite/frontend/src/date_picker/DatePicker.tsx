import { FC, useCallback, useId, useMemo } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { DatePicker as RsuiteDatePicker } from "rsuite";
import { useSyncedValue, keyOfScalar } from "../shared/useSyncedValue";
import { buildShouldDisableDate } from "../shared/dateConstraints";
import { FieldLabel } from "../shared/FieldLabel";
import { useAnchoredPopup } from "../shared/useAnchoredPopup";
import { toISOValue, parseISOValue } from "../shared/dateValue";

export type DatePickerState = {
  selected_date: string | null;
};

export type DatePickerData = {
  label: string;
  value: string | null;
  format: string;
  // True when `format` carries a time field, so the widget selects and emits a
  // "YYYY-MM-DDTHH:mm:ss" datetime instead of a "YYYY-MM-DD" date. Derived
  // Python-side from the format string so both sides share one rule.
  withTime: boolean;
  showMeridiem?: boolean;
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
  help?: string | null;
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

const DatePickerComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    label,
    value,
    format,
    withTime,
    showMeridiem,
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
    help,
    minDate,
    maxDate,
    disabledDates,
    disabledWeekdays,
    limitStartYear,
    limitEndYear,
    calendarDefaultDate,
  } = data;

  const fieldId = useId();
  const popup = useAnchoredPopup(placement);

  const [selected, emitSelected] = useSyncedValue<Date | null>(
    keyOfScalar(value),
    () => parseISOValue(value)
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
    () => (calendarDefaultDate ? parseISOValue(calendarDefaultDate) ?? undefined : undefined),
    [calendarDefaultDate]
  );

  const handleChange = useCallback(
    (newValue: Date | null) => {
      const iso = toISOValue(newValue, withTime);
      emitSelected(newValue);
      setStateValue("selected_date", iso);
    },
    [emitSelected, setStateValue, withTime]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <FieldLabel htmlFor={fieldId} label={label} help={help} />
      <RsuiteDatePicker
        id={fieldId}
        value={selected}
        onChange={handleChange}
        format={format}
        appearance={appearance}
        size={size}
        placeholder={placeholder || undefined}
        ref={popup.ref}
        onOpen={popup.onOpen}
        onClose={popup.onClose}
        placement={placement as any}
        oneTap={oneTap}
        showMeridiem={showMeridiem}
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
