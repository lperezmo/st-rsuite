import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import CarouselComponent, {
  CarouselState,
  CarouselData,
} from "./Carousel";

export default createRsuiteRenderer<CarouselState, CarouselData>(
  CarouselComponent
);
