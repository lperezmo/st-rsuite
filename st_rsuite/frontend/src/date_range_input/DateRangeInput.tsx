import { FC, useCallback, useId } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { DateRangeInput as RsuiteDateRangeInput } from "rsuite";
import { useSyncedValue, keyOfPair } from "../shared/useSyncedValue";
import { FieldLabel } from "../shared/FieldLabel";

// RSuite's DateRangeInput onChange/value use a nullable-element tuple, unlike
// DateRangePicker's [Date, Date].
type DateRangeValue = [Date | null, Date | null] | null;

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
  help?: string | null;
  locale?: string | null;
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
  const {
    label,
    startValue,
    endValue,
    format,
    character,
    size,
    placeholder,
    disabled,
    help,
  } = data;

  const fieldId = useId();

  const [selected, emitSelected] = useSyncedValue<DateRangeValue>(
    keyOfPair(startValue, endValue),
    () => {
      const s = parseDate(startValue);
      const e = parseDate(endValue);
      return s && e ? [s, e] : null;
    }
  );

  const handleChange = useCallback(
    (newValue: DateRangeValue) => {
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
      <FieldLabel htmlFor={fieldId} label={label} help={help} />
      <RsuiteDateRangeInput
        id={fieldId}
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
