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

  // MultiCascadeTree has no `disabled` prop (only per-item disabling), so honor
  // the wrapper-level flag by blocking interaction and dimming the control.
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
    </div>
  );
};

export default MultiCascadeTreeComponent;
