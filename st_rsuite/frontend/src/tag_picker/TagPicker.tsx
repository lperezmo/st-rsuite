import { FC, useCallback, useId } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { TagPicker as RsuiteTagPicker } from "rsuite";
import { useSyncedValue, keyOfList } from "../shared/useSyncedValue";
import { FieldLabel } from "../shared/FieldLabel";

export type TagPickerState = {
  selected_values: string[];
};

type Item = {
  value: string;
  label: string;
  group?: string;
};

export type TagPickerData = {
  label: string;
  items: Item[];
  value: string[];
  groupBy: string | null;
  searchable: boolean;
  virtualized: boolean;
  creatable: boolean;
  disabledItems: string[];
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
  data: TagPickerData;
  setStateValue: FrontendRendererArgs<
    TagPickerState,
    TagPickerData
  >["setStateValue"];
};

const TagPickerComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    label,
    items,
    value,
    groupBy,
    searchable,
    virtualized,
    creatable,
    disabledItems,
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

  const [selected, emitSelected] = useSyncedValue<string[]>(
    keyOfList(value),
    () => value || []
  );

  const handleChange = useCallback(
    (newValues: string[] | null) => {
      const vals = (newValues || []).map(String);
      emitSelected(vals);
      setStateValue("selected_values", vals);
    },
    [emitSelected, setStateValue]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <FieldLabel htmlFor={fieldId} label={label} help={help} />
      <RsuiteTagPicker
        id={fieldId}
        data={items}
        value={selected}
        onChange={handleChange}
        groupBy={groupBy ?? undefined}
        searchable={searchable}
        virtualized={virtualized}
        creatable={creatable}
        disabledItemValues={disabledItems || []}
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

export default TagPickerComponent;
