import { FC, useCallback } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { DateInput as RsuiteDateInput } from "rsuite";
import { useSyncedValue, keyOfScalar } from "../shared/useSyncedValue";

export type DateInputState = {
  selected_date: string | null;
};

export type DateInputData = {
  label: string;
  value: string | null;
  format: string;
  size: "lg" | "md" | "sm" | "xs";
  placeholder: string;
  disabled: boolean;
  locale?: string | null;
};

type Props = {
  data: DateInputData;
  setStateValue: FrontendRendererArgs<
    DateInputState,
    DateInputData
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

const DateInputComponent: FC<Props> = ({ data, setStateValue }) => {
  const { label, value, format, size, placeholder, disabled } = data;

  const [selected, emitSelected] = useSyncedValue<Date | null>(
    keyOfScalar(value),
    () => parseDate(value)
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
      <RsuiteDateInput
        value={selected}
        onChange={handleChange}
        format={format}
        size={size}
        placeholder={placeholder || undefined}
        disabled={disabled}
      />
    </div>
  );
};

export default DateInputComponent;
