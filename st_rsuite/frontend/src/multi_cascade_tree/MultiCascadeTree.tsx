import { FC, useCallback, useState } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { MultiCascadeTree as RsuiteMultiCascadeTree } from "rsuite";

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

  const [selected, setSelected] = useState<string[]>(value || []);

  const handleChange = useCallback(
    (newValues: string[] | null) => {
      const vals = newValues || [];
      setSelected(vals);
      setStateValue("selected_values", vals);
    },
    [setStateValue]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <RsuiteMultiCascadeTree
        data={cascadeData}
        value={selected}
        onChange={handleChange}
        cascade={cascade}
        searchable={searchable}
        columnWidth={columnWidth}
        columnHeight={columnHeight}
        disabled={disabled}
        uncheckableItemValues={uncheckableValues || []}
      />
    </div>
  );
};

export default MultiCascadeTreeComponent;
