import { FC, useCallback, useId, useMemo } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { TimePicker as RsuiteTimePicker } from "rsuite";
import { useSyncedValue, keyOfScalar } from "../shared/useSyncedValue";
import {
  buildHideHours,
  buildHideMinutes,
  buildHideSeconds,
} from "../shared/timeConstraints";
import { FieldLabel } from "../shared/FieldLabel";

export type TimePickerState = {
  selected_time: string | null;
};

export type TimePickerData = {
  label: string;
  value: string | null;
  format: string;
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
  data: TimePickerData;
  setStateValue: FrontendRendererArgs<
    TimePickerState,
    TimePickerData
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

const TimePickerComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    label,
    value,
    format,
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

  const [selected, emitSelected] = useSyncedValue<Date | null>(
    keyOfScalar(value),
    () => parseTime(value)
  );

  const handleChange = useCallback(
    (newValue: Date | null) => {
      const iso = toISOTime(newValue);
      emitSelected(newValue);
      setStateValue("selected_time", iso);
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

  // If showMeridiem is true, use 12-hour format
  const effectiveFormat = showMeridiem && format === "HH:mm" ? "hh:mm aa" : format;

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <FieldLabel htmlFor={fieldId} label={label} help={help} />
      <RsuiteTimePicker
        id={fieldId}
        value={selected}
        onChange={handleChange}
        format={effectiveFormat}
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

export default TimePickerComponent;
