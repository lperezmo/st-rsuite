/**
 * Shared field label for the date/time components.
 *
 * Centralizes two things the six labeled components previously duplicated and
 * one they lacked:
 * - consistent label styling
 * - a proper `htmlFor` association to the control's id (the old inline labels
 *   had none, so screen readers did not connect them and clicking the label did
 *   nothing)
 * - an optional help tooltip, matching Streamlit's `help=` convention
 *
 * Renders nothing when there is neither a label nor help text.
 */
import { FC } from "react";

type Props = {
  htmlFor: string;
  label?: string;
  help?: string | null;
};

export const FieldLabel: FC<Props> = ({ htmlFor, label, help }) => {
  if (!label && !help) return null;
  return (
    <label
      htmlFor={htmlFor}
      style={{
        display: "block",
        marginBottom: 4,
        fontSize: 14,
        fontWeight: 500,
      }}
    >
      {label}
      {help && (
        <span
          title={help}
          aria-label={help}
          role="img"
          style={{
            marginLeft: 5,
            cursor: "help",
            opacity: 0.55,
            fontWeight: 400,
          }}
        >
          &#9432;
        </span>
      )}
    </label>
  );
};
