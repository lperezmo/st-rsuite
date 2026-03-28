import { FC, useCallback, useState } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { CheckTree as RsuiteCheckTree } from "rsuite";

export type CheckTreeState = {
  selected_values: string[];
};

type TreeNode = {
  value: string;
  label: string;
  children?: TreeNode[];
};

export type CheckTreeData = {
  data: TreeNode[];
  value: string[];
  cascade: boolean;
  searchable: boolean;
  defaultExpandAll: boolean;
  showIndentLine: boolean;
  height: number;
  disabled: boolean;
  uncheckableValues: string[];
  locale?: string | null;
};

type Props = {
  data: CheckTreeData;
  setStateValue: FrontendRendererArgs<
    CheckTreeState,
    CheckTreeData
  >["setStateValue"];
};

const CheckTreeComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    data: treeData,
    value,
    cascade,
    searchable,
    defaultExpandAll,
    showIndentLine,
    height,
    disabled,
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
      <RsuiteCheckTree
        data={treeData}
        value={selected}
        onChange={handleChange}
        cascade={cascade}
        searchable={searchable}
        defaultExpandAll={defaultExpandAll}
        showIndentLine={showIndentLine}
        height={height}
        disabled={disabled}
        uncheckableItemValues={uncheckableValues || []}
      />
    </div>
  );
};

export default CheckTreeComponent;
