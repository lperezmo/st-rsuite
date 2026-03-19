import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import TimePickerComponent, {
  TimePickerState,
  TimePickerData,
} from "./TimePicker";

export default createRsuiteRenderer<TimePickerState, TimePickerData>(
  TimePickerComponent
);
