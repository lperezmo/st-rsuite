import { FC, useCallback, useId } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { TreePicker as RsuiteTreePicker } from "rsuite";
import { useSyncedValue, keyOfScalar } from "../shared/useSyncedValue";
import { FieldLabel } from "../shared/FieldLabel";

export type TreePickerState = {
  selected_value: string | null;
};

type TreeNode = {
  value: string;
  label: string;
  children?: TreeNode[];
};

export type TreePickerData = {
  label: string;
  data: TreeNode[];
  value: string | null;
  searchable: boolean;
  virtualized: boolean;
  defaultExpandAll: boolean;
  showIndentLine: boolean;
  onlyLeafSelectable: boolean;
  disabledItems: string[];
  height: number;
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
  data: TreePickerData;
  setStateValue: FrontendRendererArgs<
    TreePickerState,
    TreePickerData
  >["setStateValue"];
};

const TreePickerComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    label,
    data: treeData,
    value,
    searchable,
    virtualized,
    defaultExpandAll,
    showIndentLine,
    onlyLeafSelectable,
    disabledItems,
    height,
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
    (newValue: string | number | null) => {
      const val = newValue == null ? null : String(newValue);
      emitSelected(val);
      setStateValue("selected_value", val);
    },
    [emitSelected, setStateValue]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <FieldLabel htmlFor={fieldId} label={label} help={help} />
      <RsuiteTreePicker
        id={fieldId}
        data={treeData}
        value={selected}
        onChange={handleChange}
        searchable={searchable}
        virtualized={virtualized}
        defaultExpandAll={defaultExpandAll}
        showIndentLine={showIndentLine}
        onlyLeafSelectable={onlyLeafSelectable}
        disabledItemValues={disabledItems || []}
        treeHeight={height}
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

export default TreePickerComponent;
