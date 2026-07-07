import { FC, useCallback } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { CheckTree as RsuiteCheckTree } from "rsuite";
import { useSyncedValue, keyOfList } from "../shared/useSyncedValue";

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

  const [selected, emitSelected] = useSyncedValue<string[]>(
    keyOfList(value),
    () => value || []
  );

  const handleChange = useCallback(
    (newValues: (string | number)[]) => {
      const vals = newValues.map(String);
      emitSelected(vals);
      setStateValue("selected_values", vals);
    },
    [emitSelected, setStateValue]
  );

  // CheckTree has no `disabled` prop (only per-item disabling), so honor the
  // wrapper-level flag by blocking interaction and dimming the control.
  return (
    <div
      style={{
        width: "100%",
        padding: "4px 0",
        opacity: disabled ? 0.5 : 1,
        pointerEvents: disabled ? "none" : "auto",
      }}
      aria-disabled={disabled || undefined}
    >
      <RsuiteCheckTree
        data={treeData}
        value={selected}
        onChange={handleChange}
        cascade={cascade}
        searchable={searchable}
        defaultExpandAll={defaultExpandAll}
        showIndentLine={showIndentLine}
        height={height}
        uncheckableItemValues={uncheckableValues || []}
      />
    </div>
  );
};

export default CheckTreeComponent;
