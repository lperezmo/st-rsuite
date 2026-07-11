import { FC, useCallback, useId } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { Cascader as RsuiteCascader } from "rsuite";
import { useSyncedValue, keyOfScalar } from "../shared/useSyncedValue";
import { FieldLabel } from "../shared/FieldLabel";

export type CascaderState = {
  selected_value: string | null;
};

type TreeNode = {
  value: string;
  label: string;
  children?: TreeNode[];
};

export type CascaderData = {
  label: string;
  data: TreeNode[];
  value: string | null;
  parentSelectable: boolean;
  searchable: boolean;
  disabledItems: string[];
  columnWidth: number;
  columnHeight: number;
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
  data: CascaderData;
  setStateValue: FrontendRendererArgs<
    CascaderState,
    CascaderData
  >["setStateValue"];
};

const CascaderComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    label,
    data: treeData,
    value,
    parentSelectable,
    searchable,
    disabledItems,
    columnWidth,
    columnHeight,
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
      <RsuiteCascader
        id={fieldId}
        data={treeData}
        value={selected}
        onChange={handleChange}
        parentSelectable={parentSelectable}
        searchable={searchable}
        disabledItemValues={disabledItems || []}
        columnWidth={columnWidth}
        columnHeight={columnHeight}
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

export default CascaderComponent;
