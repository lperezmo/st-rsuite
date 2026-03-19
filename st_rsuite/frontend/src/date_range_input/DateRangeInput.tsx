import { FC, useCallback, useMemo, useState } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { DateRangeInput as RsuiteDateRangeInput } from "rsuite";
import type { DateRange } from "rsuite/DateRangePicker";

export type DateRangeInputState = {
  start_date: string | null;
  end_date: string | null;
};

export type DateRangeInputData = {
  label: string;
  startValue: string | null;
  endValue: string | null;
  format: string;
  character: string;
  size: "lg" | "md" | "sm" | "xs";
  placeholder: string;
  disabled: boolean;
};

type Props = {
  data: DateRangeInputData;
  setStateValue: FrontendRendererArgs<
    DateRangeInputState,
    DateRangeInputData
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

const DateRangeInputComponent: FC<Props> = ({ data, setStateValue }) => {
  const { label, startValue, endValue, format, character, size, placeholder, disabled } =
    data;

  const initialValue = useMemo<DateRange | null>(() => {
    const s = parseDate(startValue);
    const e = parseDate(endValue);
    if (s && e) return [s, e];
    return null;
  }, [startValue, endValue]);

  const [selected, setSelected] = useState<DateRange | null>(initialValue);

  const handleChange = useCallback(
    (newValue: DateRange | null) => {
      setSelected(newValue);
      if (newValue) {
        setStateValue("start_date", toISODate(newValue[0]));
        setStateValue("end_date", toISODate(newValue[1]));
      } else {
        setStateValue("start_date", null);
        setStateValue("end_date", null);
      }
    },
    [setStateValue]
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
      <RsuiteDateRangeInput
        value={selected}
        onChange={handleChange}
        format={format}
        character={character}
        size={size}
        placeholder={placeholder || undefined}
        disabled={disabled}
      />
    </div>
  );
};

export default DateRangeInputComponent;
