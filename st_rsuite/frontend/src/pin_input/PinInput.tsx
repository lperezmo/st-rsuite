import { FC, useCallback, useState } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { PinInput as RsuitePinInput } from "rsuite";

export type PinInputState = {
  pin_value: string;
};

export type PinInputData = {
  length: number;
  value: string;
  mask: boolean;
  type: string;
  size: "lg" | "md" | "sm" | "xs";
  placeholder: string;
  disabled: boolean;
  readOnly: boolean;
  otp: boolean;
  attached: boolean;
  locale?: string | null;
};

type Props = {
  data: PinInputData;
  setStateValue: FrontendRendererArgs<
    PinInputState,
    PinInputData
  >["setStateValue"];
};

const PinInputComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    length,
    value,
    mask,
    type,
    size,
    placeholder,
    disabled,
    readOnly,
    otp,
    attached,
  } = data;

  const [pinValue, setPinValue] = useState<string>(value || "");

  const handleChange = useCallback(
    (newValue: string) => {
      setPinValue(newValue);
      setStateValue("pin_value", newValue);
    },
    [setStateValue]
  );

  // Map string type to PinInput's type prop
  const pinType = type === "alphabetic"
    ? "alphabetic" as const
    : type === "alphanumeric"
    ? "alphanumeric" as const
    : "number" as const;

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <RsuitePinInput
        value={pinValue || undefined}
        onChange={(val) => handleChange(val || "")}
        length={length}
        mask={mask}
        type={pinType}
        size={size}
        placeholder={placeholder || undefined}
        disabled={disabled}
        readOnly={readOnly}
        otp={otp}
        attached={attached}
      />
    </div>
  );
};

export default PinInputComponent;
