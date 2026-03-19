import { FC, useCallback, useMemo, useState } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { DateInput as RsuiteDateInput } from "rsuite";

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

const DateInputComponent: FC<Props> = ({ data, setStateValue }) => {
  const { label, value, format, size, placeholder, disabled } = data;

  const initialValue = useMemo(
    () => (value ? new Date(value + "T00:00:00") : null),
    [value]
  );

  const [selected, setSelected] = useState<Date | null>(initialValue);

  const handleChange = useCallback(
    (newValue: Date | null) => {
      setSelected(newValue);
      setStateValue("selected_date", toISODate(newValue));
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
