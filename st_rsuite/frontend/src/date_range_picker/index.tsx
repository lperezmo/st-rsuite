import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import DateRangePickerComponent, {
  DateRangePickerState,
  DateRangePickerData,
} from "./DateRangePicker";

export default createRsuiteRenderer<DateRangePickerState, DateRangePickerData>(
  DateRangePickerComponent
);
