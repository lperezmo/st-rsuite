import { FC, useCallback, useId } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { CheckPicker as RsuiteCheckPicker } from "rsuite";
import { useSyncedValue, keyOfList } from "../shared/useSyncedValue";
import { FieldLabel } from "../shared/FieldLabel";

export type CheckPickerState = {
  selected_values: string[];
};

type Item = {
  value: string;
  label: string;
  group?: string;
};

export type CheckPickerData = {
  label: string;
  items: Item[];
  value: string[];
  groupBy: string | null;
  searchable: boolean;
  virtualized: boolean;
  disabledItems: string[];
  appearance: "default" | "subtle";
  size: "lg" | "md" | "sm" | "xs";
  placeholder: string;
  placement: string;
  disabled: boolean;
  cleanable: boolean;
  block: boolean;
  loading: boolean;
  countable: boolean;
  help?: string | null;
  locale?: string | null;
};

type Props = {
  data: CheckPickerData;
  setStateValue: FrontendRendererArgs<
    CheckPickerState,
    CheckPickerData
  >["setStateValue"];
};

const CheckPickerComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    label,
    items,
    value,
    groupBy,
    searchable,
    virtualized,
    disabledItems,
    appearance,
    size,
    placeholder,
    placement,
    disabled,
    cleanable,
    block,
    loading,
    countable,
    help,
  } = data;

  const fieldId = useId();

  const [selected, emitSelected] = useSyncedValue<string[]>(
    keyOfList(value),
    () => value || [],
  );

  const handleChange = useCallback(
    (newValues: string[] | null) => {
      const vals = (newValues || []).map(String);
      emitSelected(vals);
      setStateValue("selected_values", vals);
    },
    [emitSelected, setStateValue],
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <FieldLabel htmlFor={fieldId} label={label} help={help} />
      <RsuiteCheckPicker
        id={fieldId}
        data={items}
        value={selected}
        onChange={handleChange}
        groupBy={groupBy ?? undefined}
        searchable={searchable}
        virtualized={virtualized}
        disabledItemValues={disabledItems || []}
        appearance={appearance}
        size={size}
        placeholder={placeholder || undefined}
        placement={placement as any}
        disabled={disabled}
        cleanable={cleanable}
        block={block}
        loading={loading}
        countable={countable}
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default CheckPickerComponent;
