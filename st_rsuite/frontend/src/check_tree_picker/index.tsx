import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import CheckTreePickerComponent, {
  CheckTreePickerState,
  CheckTreePickerData,
} from "./CheckTreePicker";

export default createRsuiteRenderer<CheckTreePickerState, CheckTreePickerData>(
  CheckTreePickerComponent
);
