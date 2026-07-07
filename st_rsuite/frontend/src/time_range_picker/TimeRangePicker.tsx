import { FC, useCallback, useId, useMemo } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { TimeRangePicker as RsuiteTimeRangePicker } from "rsuite";
import type { DateRange } from "rsuite/DateRangePicker";
import { useSyncedValue, keyOfPair } from "../shared/useSyncedValue";
import {
  buildHideHours,
  buildHideMinutes,
  buildHideSeconds,
} from "../shared/timeConstraints";
import { FieldLabel } from "../shared/FieldLabel";

export type TimeRangePickerState = {
  start_time: string | null;
  end_time: string | null;
};

export type TimeRangePickerData = {
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
  showMeridiem: boolean;
  editable: boolean;
  loading: boolean;
  help?: string | null;
  hiddenHours?: number[];
  hiddenMinutes?: number[];
  hiddenSeconds?: number[];
  minHour?: number | null;
  maxHour?: number | null;
  locale?: string | null;
};

type Props = {
  data: TimeRangePickerData;
  setStateValue: FrontendRendererArgs<
    TimeRangePickerState,
    TimeRangePickerData
  >["setStateValue"];
};

function toISOTime(d: Date | null): string | null {
  if (!d || isNaN(d.getTime())) return null;
  const h = String(d.getHours()).padStart(2, "0");
  const m = String(d.getMinutes()).padStart(2, "0");
  const s = String(d.getSeconds()).padStart(2, "0");
  return `${h}:${m}:${s}`;
}

function parseTime(val: string | null): Date | null {
  if (!val) return null;
  const d = new Date(`2000-01-01T${val}`);
  return isNaN(d.getTime()) ? null : d;
}

const TimeRangePickerComponent: FC<Props> = ({ data, setStateValue }) => {
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
    showMeridiem,
    editable,
    loading,
    help,
    hiddenHours,
    hiddenMinutes,
    hiddenSeconds,
    minHour,
    maxHour,
  } = data;

  const fieldId = useId();

  const [selected, emitSelected] = useSyncedValue<DateRange | null>(
    keyOfPair(startValue, endValue),
    () => {
      const s = parseTime(startValue);
      const e = parseTime(endValue);
      return s && e ? [s, e] : null;
    }
  );

  const handleChange = useCallback(
    (newValue: DateRange | null) => {
      const s = newValue ? toISOTime(newValue[0]) : null;
      const e = newValue ? toISOTime(newValue[1]) : null;
      emitSelected(newValue);
      setStateValue("start_time", s);
      setStateValue("end_time", e);
    },
    [emitSelected, setStateValue]
  );

  const constraints = { hiddenHours, hiddenMinutes, hiddenSeconds, minHour, maxHour };
  const hideHours = useMemo(
    () => buildHideHours(constraints),
    [hiddenHours, minHour, maxHour]
  );
  const hideMinutes = useMemo(() => buildHideMinutes(constraints), [hiddenMinutes]);
  const hideSeconds = useMemo(() => buildHideSeconds(constraints), [hiddenSeconds]);

  const effectiveFormat = showMeridiem && format === "HH:mm" ? "hh:mm aa" : format;

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <FieldLabel htmlFor={fieldId} label={label} help={help} />
      <RsuiteTimeRangePicker
        id={fieldId}
        value={selected}
        onChange={handleChange}
        format={effectiveFormat}
        character={character}
        appearance={appearance}
        size={size}
        placeholder={placeholder || undefined}
        placement={placement as any}
        disabled={disabled}
        cleanable={cleanable}
        block={block}
        showMeridiem={showMeridiem}
        editable={editable}
        loading={loading}
        hideHours={hideHours}
        hideMinutes={hideMinutes}
        hideSeconds={hideSeconds}
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default TimeRangePickerComponent;
