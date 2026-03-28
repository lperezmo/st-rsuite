import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import TimelineComponent, {
  TimelineState,
  TimelineData,
} from "./Timeline";

export default createRsuiteRenderer<TimelineState, TimelineData>(
  TimelineComponent
);
