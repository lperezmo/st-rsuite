import { FC, createElement } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { Timeline as RsuiteTimeline } from "rsuite";
import { getIcon } from "../shared/icons";

export type TimelineState = {
  _nonce: number;
};

type TimelineItem = {
  content: string;
  time?: string;
  icon?: string;
  color?: string;
};

export type TimelineData = {
  items: TimelineItem[];
  align: "left" | "right" | "alternate";
  endless: boolean;
  locale?: string | null;
};

type Props = {
  data: TimelineData;
  setStateValue: FrontendRendererArgs<
    TimelineState,
    TimelineData
  >["setStateValue"];
};

function renderDot(item: TimelineItem) {
  if (!item.icon) return undefined;

  // Try react-icons registry first
  const IconComponent = getIcon(item.icon);
  if (IconComponent) {
    return createElement(IconComponent, {
      style: {
        fontSize: 16,
        color: item.color || undefined,
        background: "var(--rs-bg-card, #fff)",
        borderRadius: "50%",
        padding: 2,
      },
    });
  }

  // Fallback: render as emoji/text
  return (
    <span
      style={{
        fontSize: 16,
        color: item.color || undefined,
        background: "var(--rs-bg-card, #fff)",
        borderRadius: "50%",
        padding: 2,
        lineHeight: 1,
      }}
    >
      {item.icon}
    </span>
  );
}

const TimelineComponent: FC<Props> = ({ data }) => {
  const { items, align, endless } = data;

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <RsuiteTimeline align={align} endless={endless}>
        {items.map((item, idx) => (
          <RsuiteTimeline.Item
            key={idx}
            dot={renderDot(item)}
            time={item.time || undefined}
          >
            {item.content}
          </RsuiteTimeline.Item>
        ))}
      </RsuiteTimeline>
    </div>
  );
};

export default TimelineComponent;
