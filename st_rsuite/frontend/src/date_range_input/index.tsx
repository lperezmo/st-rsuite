import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import DateRangeInputComponent, {
  DateRangeInputState,
  DateRangeInputData,
} from "./DateRangeInput";

export default createRsuiteRenderer<DateRangeInputState, DateRangeInputData>(
  DateRangeInputComponent
);
