import { FC, useCallback } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { MultiCascadeTree as RsuiteMultiCascadeTree } from "rsuite";
import { useSyncedValue, keyOfList } from "../shared/useSyncedValue";

export type MultiCascadeTreeState = {
  selected_values: string[];
};

type CascadeOption = {
  value: string;
  label: string;
  children?: CascadeOption[];
};

export type MultiCascadeTreeData = {
  data: CascadeOption[];
  value: string[];
  cascade: boolean;
  searchable: boolean;
  columnWidth: number;
  columnHeight: number;
  disabled: boolean;
  uncheckableValues: string[];
  locale?: string | null;
};

type Props = {
  data: MultiCascadeTreeData;
  setStateValue: FrontendRendererArgs<
    MultiCascadeTreeState,
    MultiCascadeTreeData
  >["setStateValue"];
};

const MultiCascadeTreeComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    data: cascadeData,
    value,
    cascade,
    searchable,
    columnWidth,
    columnHeight,
    disabled,
    uncheckableValues,
  } = data;

  const [selected, emitSelected] = useSyncedValue<string[]>(
    keyOfList(value),
    () => value || []
  );

  const handleChange = useCallback(
    (newValues: string[] | null) => {
      const vals = newValues || [];
      emitSelected(vals);
      setStateValue("selected_values", vals);
    },
    [emitSelected, setStateValue]
  );

  // MultiCascadeTree has no wrapper-level `disabled` prop, so the wrapper is a
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
      <RsuiteMultiCascadeTree
        data={cascadeData}
        value={selected}
        onChange={handleChange}
        cascade={cascade}
        searchable={searchable}
        columnWidth={columnWidth}
        columnHeight={columnHeight}
        uncheckableItemValues={uncheckableValues || []}
      />
    </fieldset>
  );
};

export default MultiCascadeTreeComponent;
