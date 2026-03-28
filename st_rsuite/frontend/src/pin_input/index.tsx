import "rsuite/dist/rsuite-no-reset.min.css";
import { createRsuiteRenderer } from "../shared/renderer";
import PinInputComponent, {
  PinInputState,
  PinInputData,
} from "./PinInput";

export default createRsuiteRenderer<PinInputState, PinInputData>(
  PinInputComponent
);
