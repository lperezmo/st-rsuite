import { FC, useCallback, useState } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { CheckTreePicker as RsuiteCheckTreePicker } from "rsuite";

export type CheckTreePickerState = {
  selected_values: string[];
};

type TreeNode = {
  value: string;
  label: string;
  children?: TreeNode[];
};

export type CheckTreePickerData = {
  data: TreeNode[];
  value: string[];
  cascade: boolean;
  searchable: boolean;
  countable: boolean;
  appearance: "default" | "subtle";
  size: "lg" | "md" | "sm" | "xs";
  placeholder: string;
  placement: string;
  disabled: boolean;
  cleanable: boolean;
  block: boolean;
  defaultExpandAll: boolean;
  showIndentLine: boolean;
  height: number;
  uncheckableValues: string[];
  locale?: string | null;
};

type Props = {
  data: CheckTreePickerData;
  setStateValue: FrontendRendererArgs<
    CheckTreePickerState,
    CheckTreePickerData
  >["setStateValue"];
};

const CheckTreePickerComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    data: treeData,
    value,
    cascade,
    searchable,
    countable,
    appearance,
    size,
    placeholder,
    placement,
    disabled,
    cleanable,
    block,
    defaultExpandAll,
    showIndentLine,
    height,
    uncheckableValues,
  } = data;

  const [selected, setSelected] = useState<string[]>(value || []);

  const handleChange = useCallback(
    (newValues: string[]) => {
      setSelected(newValues);
      setStateValue("selected_values", newValues);
    },
    [setStateValue]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <RsuiteCheckTreePicker
        data={treeData}
        value={selected}
        onChange={handleChange}
        cascade={cascade}
        searchable={searchable}
        countable={countable}
        appearance={appearance}
        size={size}
        placeholder={placeholder || undefined}
        placement={placement as any}
        disabled={disabled}
        cleanable={cleanable}
        block={block}
        defaultExpandAll={defaultExpandAll}
        showIndentLine={showIndentLine}
        treeHeight={height}
        uncheckableItemValues={uncheckableValues || []}
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default CheckTreePickerComponent;
