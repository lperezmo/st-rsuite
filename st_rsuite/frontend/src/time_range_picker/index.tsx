import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import TimeRangePickerComponent, {
  TimeRangePickerState,
  TimeRangePickerData,
} from "./TimeRangePicker";

export default createRsuiteRenderer<TimeRangePickerState, TimeRangePickerData>(
  TimeRangePickerComponent
);
