import { FC, useCallback, useMemo, useState } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { TimeRangePicker as RsuiteTimeRangePicker } from "rsuite";
import type { DateRange } from "rsuite/DateRangePicker";

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
  } = data;

  const initialValue = useMemo<DateRange | null>(() => {
    const s = parseTime(startValue);
    const e = parseTime(endValue);
    if (s && e) return [s, e];
    return null;
  }, [startValue, endValue]);

  const [selected, setSelected] = useState<DateRange | null>(initialValue);

  const handleChange = useCallback(
    (newValue: DateRange | null) => {
      setSelected(newValue);
      if (newValue) {
        setStateValue("start_time", toISOTime(newValue[0]));
        setStateValue("end_time", toISOTime(newValue[1]));
      } else {
        setStateValue("start_time", null);
        setStateValue("end_time", null);
      }
    },
    [setStateValue]
  );

  const effectiveFormat = showMeridiem && format === "HH:mm" ? "hh:mm aa" : format;

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
      <RsuiteTimeRangePicker
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
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default TimeRangePickerComponent;
