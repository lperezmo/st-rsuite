import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import DateInputComponent, {
  DateInputState,
  DateInputData,
} from "./DateInput";

export default createRsuiteRenderer<DateInputState, DateInputData>(
  DateInputComponent
);
