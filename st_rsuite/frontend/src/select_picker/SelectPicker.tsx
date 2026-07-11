import { FC, useCallback, useId } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { SelectPicker as RsuiteSelectPicker } from "rsuite";
import { useSyncedValue, keyOfScalar } from "../shared/useSyncedValue";
import { FieldLabel } from "../shared/FieldLabel";

export type SelectPickerState = {
  selected_value: string | null;
};

type Item = {
  value: string;
  label: string;
  group?: string;
};

export type SelectPickerData = {
  label: string;
  items: Item[];
  value: string | null;
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
  help?: string | null;
  locale?: string | null;
};

type Props = {
  data: SelectPickerData;
  setStateValue: FrontendRendererArgs<
    SelectPickerState,
    SelectPickerData
  >["setStateValue"];
};

const SelectPickerComponent: FC<Props> = ({ data, setStateValue }) => {
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
    help,
  } = data;

  const fieldId = useId();

  const [selected, emitSelected] = useSyncedValue<string | null>(
    keyOfScalar(value),
    () => value
  );

  const handleChange = useCallback(
    (newValue: string | null) => {
      emitSelected(newValue);
      setStateValue("selected_value", newValue);
    },
    [emitSelected, setStateValue]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <FieldLabel htmlFor={fieldId} label={label} help={help} />
      <RsuiteSelectPicker
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
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default SelectPickerComponent;
