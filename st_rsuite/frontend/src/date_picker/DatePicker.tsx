import { FC, useCallback, useMemo, useState } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { DatePicker as RsuiteDatePicker } from "rsuite";

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
  } = data;

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
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default DatePickerComponent;
