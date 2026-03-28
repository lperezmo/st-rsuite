import { FC, useCallback, useState } from "react";
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { Carousel as RsuiteCarousel } from "rsuite";

export type CarouselState = {
  active_index: number;
};

type CarouselItem = {
  content?: string;
  src?: string;
  alt?: string;
  background?: string;
  color?: string;
};

export type CarouselData = {
  items: CarouselItem[];
  autoplay: boolean;
  autoplayInterval: number;
  placement: "top" | "bottom" | "left" | "right";
  shape: "dot" | "bar";
  activeIndex: number;
  locale?: string | null;
};

type Props = {
  data: CarouselData;
  setStateValue: FrontendRendererArgs<
    CarouselState,
    CarouselData
  >["setStateValue"];
};

const CarouselComponent: FC<Props> = ({ data, setStateValue }) => {
  const {
    items,
    autoplay,
    autoplayInterval,
    placement,
    shape,
    activeIndex,
  } = data;

  const [active, setActive] = useState<number>(activeIndex || 0);

  const handleSelect = useCallback(
    (index: number) => {
      setActive(index);
      setStateValue("active_index", index);
    },
    [setStateValue]
  );

  return (
    <div style={{ width: "100%", padding: "4px 0" }}>
      <RsuiteCarousel
        activeIndex={active}
        onSelect={handleSelect}
        autoplay={autoplay}
        autoplayInterval={autoplayInterval}
        placement={placement}
        shape={shape}
        style={{ width: "100%" }}
      >
        {items.map((item, idx) => (
          <div
            key={idx}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: "100%",
              height: "100%",
              background: item.background || "#8b5cf6",
              color: item.color || "#fff",
              fontSize: "1.25rem",
              fontWeight: 500,
              overflow: "hidden",
            }}
          >
            {item.src ? (
              <img
                src={item.src}
                alt={item.alt || ""}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                }}
              />
            ) : (
              <span style={{ padding: "2rem", textAlign: "center" }}>
                {item.content || ""}
              </span>
            )}
          </div>
        ))}
      </RsuiteCarousel>
    </div>
  );
};

export default CarouselComponent;
