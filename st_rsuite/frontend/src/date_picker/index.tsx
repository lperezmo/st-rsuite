import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import DatePickerComponent, {
  DatePickerState,
  DatePickerData,
} from "./DatePicker";

export default createRsuiteRenderer<DatePickerState, DatePickerData>(
  DatePickerComponent
);
