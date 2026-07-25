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

  // CheckTree has no wrapper-level `disabled` prop, so the wrapper is a
  // disabled <fieldset>: HTML disables every form control inside one, which
  // takes RSuite's checkboxes (and the search box) out of the tab order and
  // announces them as unavailable. pointerEvents blocks the mouse alone, and
  // without this a keyboard user could Tab in and toggle a checkbox straight
  // back to Python.
  //
  // Not `inert`, which took the subtree out of the accessibility tree along
  // with the tab order: a screen reader then announced nothing at all where
  // sighted users saw a dimmed tree with checked boxes, and the wrapper's own
  // aria-disabled went unread with it.
  //
  // Not disabledItemValues either, RSuite's own per-item disabling: it renders
  // a disabled node as unchecked whatever `value` says, so a disabled tree
  // would show none of the selection it is there to display.
  return (
    <fieldset
      disabled={disabled}
      style={{
        width: "100%",
        padding: "4px 0",
        // A fieldset carries a border, margins and a min-content floor by
        // default; reset them so it lays out exactly as the div it replaced.
        margin: 0,
        border: 0,
        minWidth: 0,
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
    </fieldset>
  );
};

export default CheckTreeComponent;
