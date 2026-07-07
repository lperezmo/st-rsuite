import { FC, useCallback } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { RadioTile as RsuiteRadioTile, RadioTileGroup } from "rsuite";
import { useSyncedValue, keyOfScalar } from "../shared/useSyncedValue";

export type RadioTileState = {
  selected_value: string | null;
};

type TileOption = {
  value: string;
  label: string;
  description?: string;
  icon?: string;
};

export type RadioTileData = {
  options: TileOption[];
  value: string | null;
  inline: boolean;
  disabled: boolean;
  locale?: string | null;
};

type Props = {
  data: RadioTileData;
  setStateValue: FrontendRendererArgs<
    RadioTileState,
    RadioTileData
  >["setStateValue"];
};

const RadioTileComponent: FC<Props> = ({ data, setStateValue }) => {
  const { options, value, inline, disabled } = data;

  const [selected, emitSelected] = useSyncedValue<string | null>(
    keyOfScalar(value),
    () => value
  );

  const handleChange = useCallback(
    (newValue: string | number | undefined) => {
      const val = newValue != null ? String(newValue) : null;
      emitSelected(val);
      setStateValue("selected_value", val);
    },
    [emitSelected, setStateValue]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <RadioTileGroup
        value={selected ?? undefined}
        onChange={handleChange}
        inline={inline}
        disabled={disabled}
      >
        {options.map((opt) => (
          <RsuiteRadioTile
            key={opt.value}
            value={opt.value}
            icon={
              opt.icon ? (
                <span style={{ fontSize: 24 }}>{opt.icon}</span>
              ) : undefined
            }
            label={opt.label}
          >
            {opt.description || ""}
          </RsuiteRadioTile>
        ))}
      </RadioTileGroup>
    </div>
  );
};

export default RadioTileComponent;
